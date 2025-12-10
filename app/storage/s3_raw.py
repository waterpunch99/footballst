import os
import json
import datetime as dt

import boto3
from botocore.exceptions import BotoCoreError, ClientError

AWS_REGION = os.getenv("AWS_REGION", "ap-northeast-2")
S3_RAW_BUCKET = os.getenv("S3_RAW_BUCKET")

_session = None
_s3_client = None


def get_s3_client():
    global _session, _s3_client
    if _s3_client is None:
        _session = boto3.session.Session(region_name=AWS_REGION)
        _s3_client = _session.client("s3")
    return _s3_client


def build_s3_key(path: str, params: dict | None = None) -> str:
   
    endpoint = path.strip("/").replace("/", "_") or "root"

    parts = [f"raw/{endpoint}"]

    if params:
        
        for k, v in sorted(params.items(), key=lambda x: x[0]):
            parts.append(f"{k}={v}")

    date_str = dt.datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
    parts.append(f"{date_str}.json")

    key = "/".join(parts)
    return key


def save_raw_json(path: str, params: dict | None, data: dict):
   
    if not S3_RAW_BUCKET:
        print("[S3] S3_RAW_BUCKET 설정이 없어 RAW 저장을 건너뜁니다.")
        return

    s3 = get_s3_client()
    key = build_s3_key(path, params)

    body = json.dumps(data, ensure_ascii=False)

    try:
        s3.put_object(
            Bucket=S3_RAW_BUCKET,
            Key=key,
            Body=body.encode("utf-8"),
            ContentType="application/json; charset=utf-8",
        )
        print(f"[S3] RAW 저장 완료: s3://{S3_RAW_BUCKET}/{key}")
    except (BotoCoreError, ClientError) as e:
        
        print(f"[S3] RAW 저장 실패: {e}")
