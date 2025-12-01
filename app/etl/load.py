from sqlalchemy.dialects.postgresql import insert

def upsert_to_postgres(df, table, engine, key_columns):
    """
    PostgreSQL UPSERT (INSERT ON CONFLICT DO NOTHING)
    key_columns = ["team_id"], ["match_id"], ["player_id"] 등 PK 컬럼 리스트
    """

    with engine.begin() as conn:
        for _, row in df.iterrows():
            stmt = insert(table).values(**row.to_dict())
            stmt = stmt.on_conflict_do_nothing(
                index_elements=key_columns
            )
            conn.execute(stmt)

    print(f"{table.name} 업서트 완료")

def load_to_postgres(df, table_name, engine):
    df.to_sql(table_name, engine, if_exists="append", index=False)
    print(f"{table_name} 저장 완료")

