import pandas as pd


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

    
    for col in ["elapsed", "team_id", "player_id", "assist_id"]:
        if col in df.columns:
            df[col] = df[col].astype("Int64")

    return df
