import pandas as pd
from app.etl.extract import extract_players
from app.etl.transform import players_to_df
from app.etl.load import upsert_to_postgres
from app.db.schema import players_table


def run_players_pipeline(engine):

    teams_df = pd.read_sql("SELECT team_id FROM teams", engine)

    if teams_df.empty:
        return

    all_players = []

    for _, row in teams_df.iterrows():
        team_id = row["team_id"]
        resp = extract_players(team_id)
        df_players = players_to_df(resp)
        all_players.append(df_players)

   
    if not all_players:
        return

    final = pd.concat(all_players, ignore_index=True)

   
    final["player_id"] = final["player_id"].astype(str)
    final["team_id"] = final["team_id"].astype(str)



    upsert_to_postgres(final, players_table, engine, ["player_id"])
    print("players 생성")
