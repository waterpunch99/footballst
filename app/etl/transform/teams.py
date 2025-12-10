import pandas as pd


def transform_teams(raw: dict) -> pd.DataFrame:
    resp = raw.get("response", [])
    rows = []

    for t in resp:
        team = t.get("team", {})
        league = t.get("league", {})

        rows.append({
            "team_id": team.get("id"),
            "name": team.get("name"),
            "country": team.get("country"),
            "league_id": league.get("id"),
            "logo": team.get("logo"),
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df = df.drop_duplicates(subset=["team_id"])
    return df
