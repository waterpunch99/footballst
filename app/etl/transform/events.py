import pandas as pd
from app.etl.transform.validators.dataframe_validator import validate_dataframe

def transform_events(raw: dict) -> pd.DataFrame:
    resp = raw.get("response", [])
    if not resp:
        return pd.DataFrame([])

    match = resp[0]
    fixture = match.get("fixture", {})
    events = match.get("events", []) or []

    match_id = fixture.get("id")
    rows = []

    for e in events:
        time_data = e.get("time") or {}
        team = e.get("team") or {}
        player = e.get("player") or {}
        assist = e.get("assist") or {}

        rows.append({
            "match_id": match_id,
            "elapsed": time_data.get("elapsed"),
            "team_id": team.get("id"),
            "player_id": player.get("id"),
            "player_name": player.get("name"),
            "assist_id": assist.get("id"),
            "assist_name": assist.get("name"),
            "type": e.get("type"),
            "detail": e.get("detail"),
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    REQUIRED = ["match_id", "elapsed", "team_id"]
    TYPES = {
        "match_id": "Int64",
        "elapsed": "Int64",
        "team_id": "Int64",
    }

    return validate_dataframe(df, REQUIRED, TYPES, "events")
