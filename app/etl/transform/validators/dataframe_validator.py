import pandas as pd

def validate_columns(df: pd.DataFrame, required_cols: list[str], table_name: str):
  
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(
            f"validation {table_name}: 컬럼 missing → {missing}"
        )

def validate_types(df: pd.DataFrame, expected_types: dict, table_name: str):
   
    for col, dtype in expected_types.items():
        if col in df.columns:
            try:
                df[col] = df[col].astype(dtype)
            except Exception:
                raise ValueError(
                    f"validation error {table_name}: column '{col}' cannot convert to {dtype}"
                )

def validate_non_empty(df: pd.DataFrame, table_name: str):
   
    if df is None or df.empty:
        raise ValueError(f"validation error {table_name}: empty df")

def validate_dataframe(df, required_cols, expected_types, table_name="unknown"):
  
    validate_columns(df, required_cols, table_name)
    validate_types(df, expected_types, table_name)
    validate_non_empty(df, table_name)
    return df
