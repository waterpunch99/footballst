import requests
from ..config.settings import API_KEY

headers = {"x-apisports-key": API_KEY}

def fetch_fixtures(league=39, season=2023):
    url = f"https://v3.football.api-sports.io/fixtures?league={league}&season={season}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data.get("response", [])
