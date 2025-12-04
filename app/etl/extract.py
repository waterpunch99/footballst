import requests
from app.config.settings import API_KEY, API_BASE_URL

headers = {"x-apisports-key": API_KEY}


def _get(path: str, params: dict | None = None):
    url = f"{API_BASE_URL}{path}"
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get("response", [])


def extract_fixtures(league=39, season=2023):
    return _get("/fixtures", {"league": league, "season": season})


def extract_teams(league=39, season=2023):
    return _get("/teams", {"league": league, "season": season})


def extract_players(team_id: int):
    return _get("/players/squads", {"team": team_id})


def extract_match_detail(match_id: int):
    return _get("/fixtures", {"id": match_id})
