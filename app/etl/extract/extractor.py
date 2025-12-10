import os
import json
import time

from app.etl.extract.api_client import request_api
from app.storage.s3_raw import save_raw_json

CACHE_DIR = "cache"
CACHE_TTL = 60 * 60 * 12 

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


def _cache_path(key: str) -> str:
    return os.path.join(CACHE_DIR, f"{key}.json")


def load_cache(key: str):
    path = _cache_path(key)
    if not os.path.exists(path):
        return None

    created = os.path.getmtime(path)
    if time.time() - created > CACHE_TTL:
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cache(key: str, data: dict):
    path = _cache_path(key)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _build_cache_key(path: str, params: dict | None) -> str:
    key = path.replace("/", "_")
    if params:
        for k, v in sorted(params.items()):
            key += f"_{k}{v}"
    return key


def extract(path: str, params: dict | None = None) -> dict:
 
    cache_key = _build_cache_key(path, params)
    cached = load_cache(cache_key)

    if cached:
        print(f"[CACHE HIT] {cache_key}")
        return cached

    print(f"[API CALL] {path}, params={params}")
    raw_json = request_api(path, params)

    
    save_cache(cache_key, raw_json)

    
    save_raw_json(path, params, raw_json)

    return raw_json



def extract_fixtures(league: int = 39, season: int = 2023) -> dict:
    return extract("/fixtures", {"league": league, "season": season})


def extract_teams(league: int = 39, season: int = 2023) -> dict:
    return extract("/teams", {"league": league, "season": season})


def extract_players(team_id: int) -> dict:
    return extract("/players/squads", {"team": team_id})


def extract_match_detail(match_id: int) -> dict:
    return extract("/fixtures", {"id": match_id})
