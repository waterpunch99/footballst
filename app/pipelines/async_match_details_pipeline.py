import asyncio
from typing import Any, Dict, List, Optional, Tuple

import aiohttp
import pandas as pd

from app.config.logger import logger
from app.db.engine import engine
from app.db.schema import fixture_details_table, events_table
from app.etl.extract.async_api_client import async_request_api
from app.etl.load.postgres_loader import upsert_dataframe
from app.etl.transform.match_details import transform_match_detail
from app.etl.transform.events import transform_events
from app.etl.extract.raw_storage.s3_raw_storage import save_raw_json

# 기존 extractor 캐시 재사용
from app.etl.extract.extractor import load_cache, save_cache


CACHE_TTL_DESC = "12h 캐시"  # 그냥 로그용


def build_cache_key(path: str, params: Optional[Dict[str, Any]]) -> str:
    """
    extractor._build_cache_key와 동일한 로직 유지.
    """
    key = path.replace("/", "_")
    if params:
        for k, v in sorted(params.items()):
            key += f"_{k}{v}"
    return key


async def _fetch_one_match_detail(
    match_id: int,
    session: aiohttp.ClientSession,
    sem: asyncio.Semaphore,
    max_retries: int = 5,
    backoff_factor: float = 1.5,
) -> Tuple[int, Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """
    단일 match_id에 대한 비동기 처리:
    1) 캐시 체크
    2) 필요 시 API 호출
    3) RAW S3 저장
    4) detail/events 변환
    실패 시 (match_id, None, None) 리턴
    """
    path = "/fixtures"
    params = {"id": int(match_id)}  # numpy.int64 방지

    cache_key = build_cache_key(path, params)
    cached = load_cache(cache_key)

    if cached:
        logger.info(f"[ASYNC MATCH] CACHE HIT match_id={match_id} ({CACHE_TTL_DESC})")
        raw = cached
    else:
        # 동시성 제한
        async with sem:
            logger.info(f"[ASYNC MATCH] API CALL 시작 match_id={match_id}")
            try:
                raw = await async_request_api(
                    session,
                    path=path,
                    params=params,
                    max_retries=max_retries,
                    backoff_factor=backoff_factor,
                )
            except Exception as e:
                logger.error(
                    f"[ASYNC MATCH] API 최종 실패 match_id={match_id} error={e}"
                )
                return match_id, None, None

        # 캐시 및 RAW S3 저장 (동기 함수이지만 비용 크지 않으니 그대로 사용)
        save_cache(cache_key, raw)
        save_raw_json(path, params, raw)

    # Transform (동기지만 CPU/IO 적당)
    try:
        df_detail = transform_match_detail(raw)
        df_events = transform_events(raw)

        if df_detail is not None and not df_detail.empty:
            logger.debug(
                f"[ASYNC MATCH] detail rows={len(df_detail)} match_id={match_id}"
            )
        if df_events is not None and not df_events.empty:
            logger.debug(
                f"[ASYNC MATCH] events rows={len(df_events)} match_id={match_id}"
            )

        return match_id, df_detail, df_events

    except Exception as e:
        logger.error(
            f"[ASYNC MATCH] Transform 실패 match_id={match_id} error={e}"
        )
        return match_id, None, None


async def _run_async_match_details(
    match_ids: List[int],
    concurrency: int = 3,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    모든 match_id에 대해 비동기 수집 수행.
    1차 실행에서 실패한 match는 retry 큐로 모아서 한 번 더 재시도.
    """
    connector = aiohttp.TCPConnector(limit=None)
    timeout = aiohttp.ClientTimeout(total=60)

    sem = asyncio.Semaphore(concurrency)

    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout,
    ) as session:
        # 1차 실행
        logger.info(
            f"async match 실행 시작: total_matches={len(match_ids)}, concurrency={concurrency}"
        )

        tasks = [
            _fetch_one_match_detail(match_id, session, sem)
            for match_id in match_ids
        ]
        results = await asyncio.gather(*tasks)

        detail_list: List[pd.DataFrame] = []
        events_list: List[pd.DataFrame] = []
        failed_ids: List[int] = []

        for match_id, df_detail, df_events in results:
            if df_detail is None and df_events is None:
                failed_ids.append(match_id)
                continue

            if df_detail is not None and not df_detail.empty:
                detail_list.append(df_detail)
            if df_events is not None and not df_events.empty:
                events_list.append(df_events)

        logger.info(
            f"async match 결과: 성공 {len(match_ids) - len(failed_ids)}건 실패 {len(failed_ids)}건"
        )

        # 실패한 match들에 대해 retry 큐 한 번 더
        if failed_ids:
            logger.warning(
                f"async match retry 큐 실행: 실패 match_id 수={len(failed_ids)}"
            )

            retry_sem = asyncio.Semaphore(max(1, concurrency // 2))

            retry_tasks = [
                _fetch_one_match_detail(
                    match_id,
                    session,
                    retry_sem,
                    max_retries=3,
                    backoff_factor=3.0,
                )
                for match_id in failed_ids
            ]
            retry_results = await asyncio.gather(*retry_tasks)

            still_failed = 0
            for match_id, df_detail, df_events in retry_results:
                if df_detail is None and df_events is None:
                    still_failed += 1
                    continue

                if df_detail is not None and not df_detail.empty:
                    detail_list.append(df_detail)
                if df_events is not None and not df_events.empty:
                    events_list.append(df_events)

            logger.info(
                f"async match retry 결과: 남은 실패 {still_failed}건 "
                f"(최종 성공 {len(match_ids) - still_failed}건)"
            )

    
    if detail_list:
        all_details = pd.concat(detail_list, ignore_index=True)
    else:
        all_details = pd.DataFrame([])

    if events_list:
        all_events = pd.concat(events_list, ignore_index=True)
    else:
        all_events = pd.DataFrame([])

    return all_details, all_events


def run_match_details_pipeline_async(
    engine,
    concurrency: int = 3,
):
    logger.info("\n[async pipeline match details 시작")

    matches = pd.read_sql("SELECT match_id FROM matches", engine)
    if matches.empty:
        logger.warning("asyncmatch 데이터 없음 스킵")
        return

    match_ids = matches["match_id"].tolist()
    logger.info(f"async pipeline match 수 = {len(match_ids)}")

    
    details_df, events_df = asyncio.run(
        _run_async_match_details(match_ids, concurrency=concurrency)
    )

    if details_df is not None and not details_df.empty:
        upsert_dataframe(
            details_df,
            fixture_details_table,
            engine,
            ["match_id"],
        )
    else:
        logger.warning("[PIPELINE ASYNC] fixture_details DataFrame 비어 있음")

    if events_df is not None and not events_df.empty:
        
        upsert_dataframe(
            events_df,
            events_table,
            engine,
            ["id"],  
        )
    else:
        logger.warning("async pipeline events df 비어 있음")

    logger.info("async pipeline match details 완료")
