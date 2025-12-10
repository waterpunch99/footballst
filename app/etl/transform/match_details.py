import pandas as pd


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
    return df
