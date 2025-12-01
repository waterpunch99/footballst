from sqlalchemy import Table, Column, Integer, BigInteger, String, DateTime, MetaData
metadata = MetaData()

teams_table = Table(
    "teams", metadata,
    Column("team_id", Integer, primary_key=True),
    Column("name", String),
    Column("country", String),
    Column("league_id", Integer),
    Column("logo", String),
)

matches_table = Table(
    "matches", metadata,
    Column("match_id", Integer, primary_key=True),
    Column("match_date", DateTime),
    Column("home_team", String),
    Column("away_team", String),
    Column("home_goals", Integer),
    Column("away_goals", Integer),
)

players_table = Table(
    "players", metadata,
    Column("player_id", BigInteger, primary_key=True),  # ID는 BigInteger 추천
    Column("team_id", BigInteger, nullable=True),       # 일부 팀 ID가 null/float일 수 있음
    Column("name", String),
    Column("age", Integer, nullable=True),              # nan 포함 → nullable 필요
    Column("number", Integer, nullable=True),           # nan 포함 가능
    Column("position", String),
    Column("photo", String),
)

fixture_details_table = Table(
    "fixture_details", metadata,
    Column("match_id", Integer, primary_key=True),
    Column("referee", String),
    Column("venue", String),
    Column("timezone", String),
    Column("date", DateTime),
)

events_table = Table(
    "events", metadata,
    Column("match_id", Integer, primary_key=True),
    Column("elapsed", Integer, primary_key=True),
    Column("player_id", Integer, primary_key=True),
    Column("team_id", Integer),
    Column("player_name", String),
    Column("assist_id", Integer),
    Column("assist_name", String),
    Column("type", String),
    Column("detail", String),
)
