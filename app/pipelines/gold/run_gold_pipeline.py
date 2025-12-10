from app.pipelines.gold.stats_pipeline import run_team_stats
from app.pipelines.gold.performance_pipeline import run_team_performance



def run_gold_pipelines(season=2023):
    print("[GOLD] Gold Layer 생성 시작")

    run_team_stats(season)
    run_team_performance(season)
    

    print("[GOLD] Gold Layer 생성 완료")
