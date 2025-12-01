import pandas as pd

def fixtures_to_df(matches):
    match_list = []
    for match in matches:
        fixture = match['fixture']
        teams = match['teams']
        goals = match['goals']

        match_list.append({
            "match_id": fixture['id'],
            "match_date": fixture['date'],
            "home_team": teams['home']['name'],
            "away_team": teams['away']['name'],
            "home_goals": goals['home'],
            "away_goals": goals['away'],
        })

    return pd.DataFrame(match_list)

def teams_to_df(teams):
    team_list = []
    for item in teams:
        team = item.get("team", {})

        team_list.append({
            "team_id": team.get("id"),
            "name": team.get("name"),
            "country": team.get("country"),
            "league_id": item.get("league", {}).get("id", 39),  # 기본 리그 39로 설정
            "logo": team.get("logo")
        })

    return pd.DataFrame(team_list)

def players_to_df(players_response):
 
    player_list = []

    if not players_response:
        return pd.DataFrame(player_list)

    team_id = players_response[0]["team"]["id"]

    for player in players_response[0]["players"]:
        player_list.append({
            "player_id": player.get("id"),
            "team_id": team_id,
            "name": player.get("name"),
            "age": player.get("age"),
            "number": player.get("number"),
            "position": player.get("position"),
            "photo": player.get("photo")
        })

    return pd.DataFrame(player_list)



def fixture_details_to_df(detail_response):
    if not detail_response:
        return pd.DataFrame([])

    f = detail_response[0]["fixture"]
    
    detail = {
        "match_id": f["id"],
        "referee": f.get("referee"),
        "venue": f.get("venue", {}).get("name"),
        "timezone": f.get("timezone"),
        "date": f.get("date")
    }

    return pd.DataFrame([detail])

def events_to_df(detail_response):
    if not detail_response:
        return pd.DataFrame([])

    events = detail_response[0].get("events", [])
    match_id = detail_response[0]["fixture"]["id"]

    event_list = []

    for e in events:
        event_list.append({
            "match_id": match_id,
            "elapsed": e.get("time", {}).get("elapsed"),
            "team_id": e.get("team", {}).get("id"),
            "player_id": e.get("player", {}).get("id"),
            "player_name": e.get("player", {}).get("name"),
            "assist_id": e.get("assist", {}).get("id"),
            "assist_name": e.get("assist", {}).get("name"),
            "type": e.get("type"),
            "detail": e.get("detail")
        })

    return pd.DataFrame(event_list)
