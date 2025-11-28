from .etl.fetch import fetch_fixtures
from .etl.transform import fixtures_to_df
from .etl.load import load_to_postgres
from .config.settings import engine


def run():
    matches = fetch_fixtures()
    df = fixtures_to_df(matches)
    load_to_postgres(df, "matches", engine)

if __name__ == "__main__":
    run()
