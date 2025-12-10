from app.etl.extract.extractor import extract_teams
from app.etl.transform.teams import transform_teams
from app.etl.load.postgres_loader import upsert_dataframe
from app.db.schema import teams_table


def run_teams_pipeline(engine, league=39, season=2023):
    print("\n[PIPELINE] Teams 시작")

    raw = extract_teams(league, season)
    df = transform_teams(raw)

    upsert_dataframe(df, teams_table, engine, ["team_id"])

    print("[PIPELINE] Teams 완료")
