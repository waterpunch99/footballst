import os
import json
import time

CACHE_DIR = "cache"
CACHE_TTL = 60 * 60 * 12  # 12 hours

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


def cache_path(key: str) -> str:
    return os.path.join(CACHE_DIR, f"{key}.json")


def load_cache(key: str):
    path = cache_path(key)
    if not os.path.exists(path):
        return None

    created = os.path.getmtime(path)
    if time.time() - created > CACHE_TTL:
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cache(key: str, data: dict):
    path = cache_path(key)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
