from app.etl.extract.api_client import request_api
from app.etl.extract.cache.local_cache import load_cache, save_cache
from app.etl.extract.raw_storage.s3_raw_storage import save_raw_json


def build_cache_key(path: str, params: dict | None) -> str:
    key = path.strip("/").replace("/", "_")
    if params:
        for k, v in sorted(params.items()):
            key += f"_{k}{v}"
    return key


def extract(path: str, params: dict | None = None, use_cache=True) -> dict:
 
    cache_key = build_cache_key(path, params)

    
    if use_cache:
        cached = load_cache(cache_key)
        if cached:
            print(f"cache hit {cache_key}")
            return cached

    
    raw_json = request_api(path, params)

    
    if use_cache:
        save_cache(cache_key, raw_json)

   
    save_raw_json(path, params, raw_json)

    return raw_json



def extract_fixtures(league=39, season=2023):
    return extract("/fixtures", {"league": league, "season": season})


def extract_teams(league=39, season=2023):
    return extract("/teams", {"league": league, "season": season})


def extract_players(team_id: int):
    return extract("/players/squads", {"team": team_id})


def extract_match_detail(match_id: int):
    return extract("/fixtures", {"id": match_id})
