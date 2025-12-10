import pandas as pd

from app.etl.extract.extractor import extract_players
from app.etl.transform.players import transform_players
from app.etl.load.postgres_loader import upsert_dataframe
from app.db.schema import players_table


def run_players_pipeline(engine):
    print("\n파이프라인 Players 시작")

    teams_df = pd.read_sql("SELECT team_id FROM teams", engine)
    if teams_df.empty:
        print("파이프라인 teams 데이터 없음  스킵")
        return

    all_players = []

    for _, row in teams_df.iterrows():
        team_id = row["team_id"]
        raw = extract_players(team_id)
        df = transform_players(raw)

        if not df.empty:
            all_players.append(df)

    if not all_players:
        print("파이프라인 players 없음  완료")
        return

    final_df = pd.concat(all_players, ignore_index=True)

    upsert_dataframe(final_df, players_table, engine, ["player_id"])

    print("파이프라인 Players 완료")
