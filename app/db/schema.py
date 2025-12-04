from sqlalchemy import (
    Table, Column, Integer, BigInteger, String,
    DateTime, MetaData
)

metadata = MetaData()

teams_table = Table(
    "teams",
    metadata,
    Column("team_id", Integer, primary_key=True),
    Column("name", String),
    Column("country", String),
    Column("league_id", Integer),
    Column("logo", String),
)

matches_table = Table(
    "matches",
    metadata,
    Column("match_id", Integer, primary_key=True),
    Column("match_date", DateTime),
    Column("home_team_id", Integer),
    Column("away_team_id", Integer),
    Column("home_goals", Integer),
    Column("away_goals", Integer),
)



players_table = Table(
    "players",
    metadata,
    Column("player_id", String, primary_key=True),
    Column("team_id", String),
    Column("name", String),
    Column("age", String),  
    Column("number", String),
    Column("position", String),
    Column("photo", String),
)



fixture_details_table = Table(
    "fixture_details",
    metadata,
    Column("match_id", Integer, primary_key=True),
    Column("referee", String),
    Column("venue", String),
    Column("timezone", String),
    Column("date", DateTime),
)

events_table = Table(
    "events",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),
    Column("match_id", Integer),
    Column("elapsed", Integer),
    Column("team_id", Integer),
    Column("player_id", Integer),
    Column("player_name", String),
    Column("assist_id", Integer),
    Column("assist_name", String),
    Column("type", String),
    Column("detail", String),
)
