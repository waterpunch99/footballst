import time
import pandas as pd

from app.etl.extract import extract_match_detail
from app.etl.transform import fixture_details_to_df, events_to_df
from app.etl.load import upsert_to_postgres
from app.db.schema import fixture_details_table, events_table


def run_match_details_pipeline(engine, sleep_sec=0.5):

    matches = pd.read_sql("SELECT match_id FROM matches", engine)

    detail_list = []
    event_list = []

    for i, row in matches.iterrows():
        match_id = row["match_id"]

        raw = extract_match_detail(match_id)
        df_detail = fixture_details_to_df(raw)
        df_event = events_to_df(raw)

        if not df_detail.empty:
            detail_list.append(df_detail)
        if not df_event.empty:
            event_list.append(df_event)

        if i % 3 == 0:
            time.sleep(sleep_sec)

    if detail_list:
        upsert_to_postgres(
            pd.concat(detail_list, ignore_index=True),
            fixture_details_table,
            engine,
            ["match_id"]
        )

    if event_list:
        upsert_to_postgres(
            pd.concat(event_list, ignore_index=True),
            events_table,
            engine,
            ["id"]
        )

    print("match_detail 생성")
