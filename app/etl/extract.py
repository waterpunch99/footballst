import time
import os
import json
import requests
from requests.exceptions import RequestException
from app.config.settings import API_KEY, API_BASE_URL

CACHE_DIR = "cache"
CACHE_TTL = 60 * 60 * 12  

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

headers = {"x-apisports-key": API_KEY}



def load_cache(cache_name):
    path = os.path.join(CACHE_DIR, f"{cache_name}.json")
    if not os.path.exists(path):
        return None

    created = os.path.getmtime(path)
    if time.time() - created > CACHE_TTL:
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cache(cache_name, data):
    path = os.path.join(CACHE_DIR, f"{cache_name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)



def safe_request(url, params=None, retries=5, backoff_factor=1.5):
    attempt = 0

    while attempt < retries:
        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=10
            )

            
            if response.status_code == 429:
                wait = (backoff_factor ** attempt)
                print(f"[429] rate limit. waiting {wait:.1f}s...")
                time.sleep(wait)
                attempt += 1
                continue

            response.raise_for_status()
            return response.json()

        except RequestException as e:
            wait = (backoff_factor ** attempt)
            print(f" {attempt + 1}/{retries}, {wait:.1f}s | error={e}")
            time.sleep(wait)
            attempt += 1

    raise Exception(f"API request failed after {retries} retries: {url}")



def cached_get(path: str, params: dict | None = None):
    
    cache_key = path.replace("/", "_")
    if params:
        for k, v in params.items():
            cache_key += f"_{k}{v}"

    
    cached = load_cache(cache_key)
    if cached is not None:
        print(f" cache {cache_key}")
        return cached.get("response", [])

    
    url = f"{API_BASE_URL}{path}"
    print(f"{url}, params={params}")
    data = safe_request(url, params=params)

   
    save_cache(cache_key, data)

    return data.get("response", [])



def extract_fixtures(league=39, season=2023):
    return cached_get("/fixtures", {"league": league, "season": season})


def extract_teams(league=39, season=2023):
    return cached_get("/teams", {"league": league, "season": season})


def extract_players(team_id: int):
    return cached_get("/players/squads", {"team": team_id})


def extract_match_detail(match_id: int):
    return cached_get("/fixtures", {"id": match_id})
