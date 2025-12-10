import pandas as pd
from app.etl.transform.validators.dataframe_validator import validate_dataframe

def transform_match_detail(raw: dict) -> pd.DataFrame:
    resp = raw.get("response", [])
    if not resp:
        return pd.DataFrame([])

    f = resp[0].get("fixture", {})

    df = pd.DataFrame([{
        "match_id": f.get("id"),
        "referee": f.get("referee"),
        "venue": (f.get("venue") or {}).get("name"),
        "timezone": f.get("timezone"),
        "date": f.get("date"),
    }])

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    REQUIRED = ["match_id", "date"]
    TYPES = {
        "match_id": "Int64",
    }

    return validate_dataframe(df, REQUIRED, TYPES, "fixture_details")
