from .etl.fetch import fetch_fixtures, fetch_teams, fetch_players, fetch_match_detail
from .etl.transform import fixtures_to_df, teams_to_df, players_to_df, fixture_details_to_df, events_to_df
from .etl.load import upsert_to_postgres
from .config.settings import engine

from .models import (
    teams_table,
    matches_table,
    players_table,
    fixture_details_table,
    events_table
)
import pandas as pd


def run_teams_pipeline():
    
    teams = fetch_teams()
    df_teams = teams_to_df(teams)
    upsert_to_postgres(df_teams, teams_table, engine, ["team_id"])
    


def run_fixtures_pipeline():
    
    matches = fetch_fixtures()
    df_matches = fixtures_to_df(matches)
    upsert_to_postgres(df_matches, matches_table, engine, ["match_id"])
    


def run_players_pipeline():
    teams_df = pd.read_sql("SELECT team_id FROM teams", engine)

    all_players = []

    for _, row in teams_df.iterrows():
        team_id = row["team_id"]
        players_response = fetch_players(team_id)
        df_players = players_to_df(players_response)
        all_players.append(df_players)

    final_df = pd.concat(all_players, ignore_index=True)
    upsert_to_postgres(final_df, players_table, engine, ["player_id"])


def run_match_details_pipeline():
    

    matches_df = pd.read_sql("SELECT match_id FROM matches", engine)

    all_details = []
    all_events = []

    for _, row in matches_df.iterrows():
        match_id = row["match_id"]

        detail_response = fetch_match_detail(match_id)

        df_detail = fixture_details_to_df(detail_response)
        df_events = events_to_df(detail_response)

        all_details.append(df_detail)
        all_events.append(df_events)

    upsert_to_postgres(pd.concat(all_details, ignore_index=True),
                       fixture_details_table, engine, ["match_id"])

    upsert_to_postgres(pd.concat(all_events, ignore_index=True),
                       events_table, engine, ["match_id", "elapsed", "player_id"])

    
def run():
    run_teams_pipeline()
    run_fixtures_pipeline()
    run_players_pipeline()
    run_match_details_pipeline()


if __name__ == "__main__":
    run()