import pandas as pd


def transform_players(raw: dict) -> pd.DataFrame:
    resp = raw.get("response", [])

    if not resp:
        return pd.DataFrame([])

    block = resp[0]
    team = block.get("team", {})
    players = block.get("players", [])

    rows = []
    for p in players:
        rows.append({
            "player_id": str(p.get("id")),
            "team_id": team.get("id"),
            "name": p.get("name"),
            "age": p.get("age"),
            "number": p.get("number"),
            "position": p.get("position"),
            "photo": p.get("photo"),
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df["player_id"] = df["player_id"].astype(str)
    df["team_id"] = df["team_id"].astype("Int64")
    return df
