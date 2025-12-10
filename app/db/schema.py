from sqlalchemy import (
    Table, Column, Integer, BigInteger, String,
    DateTime, MetaData,Float
)

from sqlalchemy.dialects.postgresql import JSONB
import datetime as dt



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
    Column("team_id", Integer),
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

    Column("player_id", String),
    Column("player_name", String),

    Column("assist_id", String),
    Column("assist_name", String),

    Column("type", String),
    Column("detail", String),
)



team_stats_table = Table(
    "team_stats",
    metadata,
    Column("team_id", Integer, primary_key=True),
    Column("season", Integer, primary_key=True),
    Column("total_matches", Integer),
    Column("wins", Integer),
    Column("draws", Integer),
    Column("losses", Integer),
    Column("goals_for", Integer),
    Column("goals_against", Integer),
    Column("goal_diff", Integer),
    Column("win_rate", Float),
    Column("recent5_win_rate", Float),
    Column("recent5_goal_diff", Float),
    Column("updated_at", DateTime),
)

team_performance_table = Table(
    "team_performance",
    metadata,
    Column("team_id", Integer, primary_key=True),
    Column("season", Integer, primary_key=True),
    Column("goals_per_match", Float),
    Column("goals_conceded_per_match", Float),
    Column("goal_diff_per_match", Float),
    Column("updated_at", DateTime),
)


raw_files_table = Table(
    "raw_files",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("s3_key", String, nullable=False),
    Column("category", String, nullable=False),
    Column("params", JSONB),
    Column("file_size", Integer),
    Column("status", String, default="success"),
    Column("created_at", DateTime, default=dt.datetime.utcnow)
)
