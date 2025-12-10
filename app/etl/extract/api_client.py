import os
import time
import requests
from requests.exceptions import RequestException

from app.config.settings import API_KEY, API_BASE_URL

headers = {"x-apisports-key": API_KEY}


def request_api(path: str, params: dict | None = None,
                retries: int = 5, backoff_factor: float = 1.5) -> dict:
    """
    외부 API 호출만 담당.
    Transform, DB 적재, 캐시 등은 절대 포함하지 않는다.
    """
    url = f"{API_BASE_URL}{path}"
    attempt = 0

    while attempt < retries:
        try:
            response = requests.get(
                url, headers=headers, params=params, timeout=10
            )

            # rate limit → exponential backoff
            if response.status_code == 429:
                wait = backoff_factor ** attempt
                print(f"[429] Rate limit → {wait:.1f}s 대기")
                time.sleep(wait)
                attempt += 1
                continue

            response.raise_for_status()
            return response.json()

        except RequestException as e:
            wait = backoff_factor ** attempt
            print(f"[ERROR] API 재시도 {attempt+1}/{retries}, {wait:.1f}s | {e}")
            time.sleep(wait)
            attempt += 1

    raise Exception(f"API 호출 실패: {url}")
