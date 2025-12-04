from app.etl.extract import extract_teams
from app.etl.transform import teams_to_df
from app.etl.load import upsert_to_postgres
from app.db.schema import teams_table


def run_teams_pipeline(engine, league=39, season=2023):

    df = teams_to_df(extract_teams(league, season))
    df = df.drop_duplicates(subset=["team_id"])

    upsert_to_postgres(df, teams_table, engine, ["team_id"])

    print("[teams 생성")
