import os
import time
import requests
from requests.exceptions import RequestException
from app.config.logger import logger
from app.config.settings import API_KEY, API_BASE_URL

headers = {"x-apisports-key": API_KEY}


def request_api(path: str, params: dict | None = None,
                retries: int = 5, backoff_factor: float = 1.5) -> dict:

    url = f"{API_BASE_URL}{path}"
    attempt = 0
    logger.info(f" extract api 요청 path={path} params={params}")

    while attempt < retries:
        try:
            response = requests.get(
                url, headers=headers, params=params, timeout=10
            )

            # rate limit → exponential backoff
            if response.status_code == 429:
                wait = backoff_factor ** attempt
                logger.warning(f"429 Rate Limit  {wait:.1f}s 대기")
                time.sleep(wait)
                attempt += 1
                continue

            response.raise_for_status()
            logger.info(f"extract api 요청 성공: {path} params={params}")
            return response.json()

        except RequestException as e:
            wait = backoff_factor ** attempt
            logger.error(f"[extract api 오류 attempt={attempt+1}/{retries} → {e}")
            time.sleep(wait)
            attempt += 1
    logger.critical(f"extract 실패 path={path} params={params}")
    raise Exception(f"api 실패: {url}")
