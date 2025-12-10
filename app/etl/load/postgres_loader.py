import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError


def upsert_dataframe(df: pd.DataFrame, table, engine, key_cols: list[str]):
    """
    DataFrame → PostgreSQL Upsert
    key_cols : primary key or unique key column names
    """

    if df is None or df.empty:
        print(f"[LOAD] {table.name}: 빈 DataFrame, 스킵")
        return

   
    records = df.to_dict(orient="records")

    
    with engine.begin() as conn:
        try:
            stmt = insert(table).values(records)

            
            update_dict = {
                c.name: stmt.excluded[c.name]
                for c in table.c
                if c.name not in key_cols    
            }

            stmt = stmt.on_conflict_do_update(
                index_elements=key_cols,
                set_=update_dict
            )

            conn.execute(stmt)
            print(f"[LOAD] {table.name}: {len(df)}건 upsert 완료")

        except SQLAlchemyError as e:
            print(f"[ERROR] {table.name} upsert 실패 → {e}")
