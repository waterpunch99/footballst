from app.db.schema import metadata
from app.db.engine import engine

from app.pipelines.teams_pipeline import run_teams_pipeline
from app.pipelines.fixtures_pipeline import run_fixtures_pipeline
from app.pipelines.players_pipeline import run_players_pipeline
from app.pipelines.match_details_pipeline import run_match_details_pipeline


def init_db():
    metadata.create_all(engine)
    print("[DB] 테이블 생성 완료")


def run_all(league=39, season=2023):
    init_db()

    run_teams_pipeline(engine, league, season)
    run_fixtures_pipeline(engine, league, season)
    run_players_pipeline(engine)
    run_match_details_pipeline(engine)
