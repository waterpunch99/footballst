import pandas as pd
from sqlalchemy.dialects.postgresql import insert


def upsert_to_postgres(df, table, engine, key_cols):
    if df.empty:
        print(f" {table.name}: df 없음")
        return

    records = df.to_dict(orient="records")

    with engine.begin() as conn:
        stmt = insert(table).values(records)
        stmt = stmt.on_conflict_do_nothing(index_elements=key_cols)
        conn.execute(stmt)

    print(f"{table.name}완료")
