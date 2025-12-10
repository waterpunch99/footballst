from app.etl.extract.extractor import extract_fixtures
from app.etl.transform.fixtures import transform_fixtures
from app.etl.load.postgres_loader import upsert_dataframe
from app.db.schema import matches_table


def run_fixtures_pipeline(engine, league=39, season=2023):
    print("\n파이프라인 Fixtures 시작")

    raw = extract_fixtures(league, season)
    df = transform_fixtures(raw)

    upsert_dataframe(df, matches_table, engine, ["match_id"])

    print("파이프라인 Fixtures 완료")
