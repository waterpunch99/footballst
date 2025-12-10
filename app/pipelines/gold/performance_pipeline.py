import pandas as pd
from datetime import datetime
from app.db.engine import engine
from app.db.schema import team_stats_table, team_performance_table
from app.etl.load.postgres_loader import upsert_dataframe

def run_team_performance(season=2023):
    print("[GOLD] team_performance 계산 시작")

    stats = pd.read_sql("SELECT * FROM team_stats", engine)
    stats = stats[stats["season"] == season]

    if stats.empty:
        print("[GOLD] team_stats 비어 있음 → 먼저 stats 실행 필요")
        return

    rows = []
    for _, row in stats.iterrows():
        total = row["total_matches"]
        if total == 0:
            continue

        rows.append({
            "team_id": row["team_id"],
            "season": season,
            "goals_per_match": row["goals_for"] / total,
            "goals_conceded_per_match": row["goals_against"] / total,
            "goal_diff_per_match": row["goal_diff"] / total,
            "updated_at": datetime.utcnow()
        })

    df_perf = pd.DataFrame(rows)
    upsert_dataframe(df_perf, team_performance_table, engine, ["team_id", "season"])

    print("[GOLD] team_performance 완료")
