import pandas as pd


def transform_fixtures(raw: dict) -> pd.DataFrame:
    """
    raw json → matches DataFrame
    """
    resp = raw.get("response", [])
    rows = []

    for m in resp:
        fixture = m.get("fixture", {})
        teams = m.get("teams", {})
        goals = m.get("goals", {})

        home = teams.get("home", {})
        away = teams.get("away", {})

        rows.append({
            "match_id": fixture.get("id"),
            "match_date": fixture.get("date"),
            "home_team_id": home.get("id"),
            "away_team_id": away.get("id"),
            "home_goals": goals.get("home"),
            "away_goals": goals.get("away"),
        })

    df = pd.DataFrame(rows)
    if df.empty:
        return df

    df["match_date"] = pd.to_datetime(df["match_date"], errors="coerce")
    return df
