import pandas as pd


def fixtures_to_df(matches):
    rows = []

    for m in matches:
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
            "away_goals": goals.get("away")
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df["match_date"] = pd.to_datetime(df["match_date"])

    return df


def teams_to_df(teams):
    return pd.DataFrame([{
        "team_id": t.get("team", {}).get("id"),
        "name": t.get("team", {}).get("name"),
        "country": t.get("team", {}).get("country"),
        "league_id": t.get("league", {}).get("id", 39),
        "logo": t.get("team", {}).get("logo")
    } for t in teams])


def players_to_df(resp):
    if not resp:
        return pd.DataFrame([])

    block = resp[0]
    team_id = block.get("team", {}).get("id")
    players = block.get("players", [])

    return pd.DataFrame([{
        "player_id": str(p.get("id")),
        "team_id": p.get(team_id),
        "name": p.get("name"),
        "age": p.get("age"),
        "number": p.get("number"),
        "position": p.get("position"),
        "photo": p.get("photo")
    } for p in players])


def fixture_details_to_df(resp):
    if not resp:
        return pd.DataFrame([])

    f = resp[0].get("fixture", {})

    df = pd.DataFrame([{
        "match_id": f.get("id"),
        "referee": f.get("referee"),
        "venue": f.get("venue", {}).get("name"),
        "timezone": f.get("timezone"),
        "date": f.get("date"),
    }])

    df["date"] = pd.to_datetime(df["date"])
    return df


import pandas as pd


def events_to_df(resp):
    if not resp:
        return pd.DataFrame([])

    match = resp[0]
    fixture = match.get("fixture", {})
    events = match.get("events", []) or []

    match_id = fixture.get("id")

    rows = []
    for e in events:
        time = e.get("time") or {}
        team = e.get("team") or {}
        player = e.get("player") or {}
        assist = e.get("assist") or {}

        rows.append({
            "match_id": match_id,
            "elapsed": time.get("elapsed"),          
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


