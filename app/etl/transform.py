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
