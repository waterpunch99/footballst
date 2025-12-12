import asyncio
from typing import Any, Dict, Optional

import aiohttp

from app.config.settings import API_KEY, API_BASE_URL
from app.config.logger import logger

headers = {"x-apisports-key": API_KEY}


async def async_request_api(
    session: aiohttp.ClientSession,
    path: str,
    params: Optional[Dict[str, Any]] = None,
    max_retries: int = 5,
    backoff_factor: float = 1.5,
) -> Dict[str, Any]:
   
    url = f"{API_BASE_URL}{path}"

    for attempt in range(max_retries):
        try:
            async with session.get(
                url,
                headers=headers,
                params=params,
                timeout=10,
            ) as resp:
                status = resp.status

                if status == 429:
                    wait = backoff_factor ** attempt
                    logger.warning(
                        f"async extract 429 Rate Limit (attempt={attempt+1}/{max_retries}) "
                        f" {wait:.1f}s 대기 path={path} params={params}"
                    )
                    await asyncio.sleep(wait)
                    continue

                if status >= 500:
                    
                    wait = backoff_factor ** attempt
                    logger.error(
                        f"async extract 서버 dpfj status={status} (attempt={attempt+1}/{max_retries}) "
                        f" {wait:.1f}s 대기 path={path} params={params}"
                    )
                    await asyncio.sleep(wait)
                    continue

                resp.raise_for_status()
                data = await resp.json()
                logger.info(f"async extract api 성공 path={path} params={params}")
                return data

        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            wait = backoff_factor ** attempt
            logger.error(
                f"async extract 네트워크,타임아웃 오류 (attempt={attempt+1}/{max_retries}) "
                f"{wait:.1f}s 대기 path={path} params={params} error={e}"
            )
            await asyncio.sleep(wait)

   
    logger.critical(
        f"async extract 실패 path={path} params={params} (max_retries={max_retries})"
    )
    raise Exception(f"async extract api 호출 실패: {url}")
