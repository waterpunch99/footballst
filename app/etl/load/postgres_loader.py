import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError
from app.config.logger import logger
from app.etl.load.error_log import log_load_error
from app.etl.load.dead_letter import save_dead_letter


def upsert_dataframe(df: pd.DataFrame, table, engine, key_cols: list[str]):
 

    if df is None or df.empty:
        logger.warning(f"load {table.name} 빈 df 스킵")
        return

    records = df.to_dict(orient="records")

    success = 0
    fail = 0

    with engine.begin() as conn:
        for r in records:
            try:
                stmt = insert(table).values(r)

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
                success += 1

            except SQLAlchemyError as e:
                fail += 1
                logger.error(f"load 실패: {e}")

                # Dead-letter 저장
                save_dead_letter(table.name, r, str(e))

                # Error log 기록
                log_load_error(table.name, e, r)

    logger.info(f"load {table.name} 성공 {success}건, 실패 {fail}건")
