from app.pipelines.run_all import run_all         
from app.pipelines.gold.run_gold_pipeline import run_gold_pipelines 


def main(league=39, season=2023):
    
    run_all(league=league, season=season)

   
    run_gold_pipelines(season=season)


if __name__ == "__main__":
    main()
