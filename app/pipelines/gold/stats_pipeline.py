import pandas as pd
from datetime import datetime
from app.db.engine import engine
from app.db.schema import matches_table, fixture_details_table, team_stats_table
from app.etl.load.postgres_loader import upsert_dataframe


def run_team_stats(season=2023):
    print("[GOLD] team_stats 계산 시작")

    # Silver 레이어 수집
    matches = pd.read_sql(f"SELECT * FROM matches", engine)
    details = pd.read_sql(f"SELECT * FROM fixture_details", engine)

    if matches.empty or details.empty:
        print("[GOLD] Silver 레이어 데이터 부족")
        return

    # 날짜 붙이기
    df = matches.merge(details[["match_id", "date"]], on="match_id", how="left")

    # home/away 각각을 "팀 관점"으로 변환
    home_df = df.rename(columns={
        "home_team_id": "team_id",
        "home_goals": "goals_for",
        "away_goals": "goals_against"
    })[["team_id", "match_id", "date", "goals_for", "goals_against"]]

    away_df = df.rename(columns={
        "away_team_id": "team_id",
        "away_goals": "goals_for",
        "home_goals": "goals_against"
    })[["team_id", "match_id", "date", "goals_for", "goals_against"]]

    combined = pd.concat([home_df, away_df], ignore_index=True)
    combined["goal_diff"] = combined["goals_for"] - combined["goals_against"]

    # 결과(win/draw/loss)
    combined["result"] = combined.apply(
        lambda x: "win" if x.goals_for > x.goals_against
        else ("loss" if x.goals_for < x.goals_against else "draw"),
        axis=1
    )

    result_map = {"win": 1, "draw": 0, "loss": 0}

    # 시즌 단위 그룹핑
    groups = combined.groupby("team_id")

    rows = []
    for team_id, g in groups:
        g_sorted = g.sort_values("date")

        total_matches = len(g)
        wins = (g["result"] == "win").sum()
        draws = (g["result"] == "draw").sum()
        losses = (g["result"] == "loss").sum()
        goals_for = g["goals_for"].sum()
        goals_against = g["goals_against"].sum()

        # 최근 5경기
        recent5 = g_sorted.tail(5)
        recent5_win_rate = (recent5["result"] == "win").mean()
        recent5_goal_diff = recent5["goal_diff"].mean()

        rows.append({
            "team_id": team_id,
            "season": season,
            "total_matches": total_matches,
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "goal_diff": goals_for - goals_against,
            "win_rate": wins / total_matches if total_matches > 0 else 0,
            "recent5_win_rate": recent5_win_rate,
            "recent5_goal_diff": recent5_goal_diff,
            "updated_at": datetime.utcnow()
        })

    df_stats = pd.DataFrame(rows)
    upsert_dataframe(df_stats, team_stats_table, engine, ["team_id", "season"])

    print("[GOLD] team_stats 완료")
