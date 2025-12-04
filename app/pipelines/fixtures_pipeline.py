from app.etl.extract import extract_fixtures
from app.etl.transform import fixtures_to_df
from app.etl.load import upsert_to_postgres
from app.db.schema import matches_table


def run_fixtures_pipeline(engine, league=39, season=2023):

    df = fixtures_to_df(extract_fixtures(league, season))
    upsert_to_postgres(df, matches_table, engine, ["match_id"])

    print("fixture 생성")
