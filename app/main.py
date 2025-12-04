from app.db.engine import engine
from app.db.schema import metadata
from app.pipelines.teams_pipeline import run_teams_pipeline
from app.pipelines.fixtures_pipeline import run_fixtures_pipeline
from app.pipelines.players_pipeline import run_players_pipeline
from app.pipelines.match_details_pipeline import run_match_details_pipeline


def init_db():
    metadata.create_all(engine)


def run_all():
    init_db()

    run_teams_pipeline(engine)
    run_fixtures_pipeline(engine)
    run_players_pipeline(engine)
    run_match_details_pipeline(engine)


if __name__ == "__main__":
    run_all()
