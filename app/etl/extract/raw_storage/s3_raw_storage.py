import os
import json
import datetime as dt

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from app.db.engine import engine
from app.db.schema import raw_files_table


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


def build_daily_s3_key(path: str, params: dict | None = None) -> str:
   
    endpoint = path.strip("/").replace("/", "_") or "root"

    parts = [f"raw/{endpoint}"]

    if params:
        for k, v in sorted(params.items()):
            parts.append(f"{k}={v}")

   
    today = dt.datetime.utcnow().strftime("%Y-%m-%d")
    parts.append(f"date={today}")

    
    parts.append("data.json")

    key = "/".join(parts)
    return key


def save_raw_json(path: str, params: dict | None, data: dict):
  
    if not S3_RAW_BUCKET:
        print("S3 저장 생략 S3_RAW_BUCKET 없음")
        return

    s3 = get_s3_client()
    key = build_daily_s3_key(path, params)

    body = json.dumps(data, ensure_ascii=False).encode("utf-8")

    try:
        s3.put_object(
            Bucket=S3_RAW_BUCKET,
            Key=key,
            Body=body,
            ContentType="application/json; charset=utf-8",
        )
        print(f"S3 raw 저장 완료: s3://{S3_RAW_BUCKET}/{key}")

        clean_params = normalize_params(params)

        
        save_raw_file_metadata(key, path, clean_params, len(body))

    except (BotoCoreError, ClientError) as e:
        print(f"S3 raw 저장 실패: {e}")
        save_raw_file_metadata(key, path, params, 0, status="failed")

def save_raw_file_metadata(key, path, params, file_size, status="success"):
    from sqlalchemy import insert

    record = {
        "s3_key": key,
        "category": path.strip("/").replace("/", "_"),
        "params": params,
        "file_size": file_size,
        "status": status
    }

    with engine.begin() as conn:
        stmt = insert(raw_files_table).values(record)
        conn.execute(stmt)

def normalize_params(params: dict | None):
 
    if not params:
        return params

    normalized = {}
    for k, v in params.items():
        
        try:
            if hasattr(v, "item"):
                v = v.item()
        except Exception:
            pass

        if isinstance(v, (int, float, str)) or v is None:
            normalized[k] = v
        else:
           
            try:
                normalized[k] = json.loads(json.dumps(v, default=str))
            except:
                normalized[k] = str(v)

    return normalized
