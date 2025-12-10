import pandas as pd

from app.etl.extract.extractor import extract_match_detail
from app.etl.transform.match_details import transform_match_detail
from app.etl.transform.events import transform_events
from app.etl.load.postgres_loader import upsert_dataframe
from app.db.schema import fixture_details_table, events_table


def run_match_details_pipeline(engine, sleep_sec=0.5):
    print("\n파이프라인 Match Details 시작")

    matches = pd.read_sql("SELECT match_id FROM matches", engine)
    if matches.empty:
        print("파이프라인 match 데이터 없음 스킵")
        return

    detail_list = []
    event_list = []

    for i, row in matches.iterrows():
        match_id = row["match_id"]

        raw = extract_match_detail(match_id)

        df_detail = transform_match_detail(raw)
        df_events = transform_events(raw)

        if not df_detail.empty:
            detail_list.append(df_detail)

        if not df_events.empty:
            event_list.append(df_events)

        
        if i % 3 == 0:
            import time
            time.sleep(sleep_sec)

    if detail_list:
        upsert_dataframe(
            pd.concat(detail_list, ignore_index=True),
            fixture_details_table,
            engine,
            ["match_id"]
        )

    if event_list:
        upsert_dataframe(
            pd.concat(event_list, ignore_index=True),
            events_table,
            engine,
            ["id"]   
        )

    print("파이프라인 Match Details 완료")
