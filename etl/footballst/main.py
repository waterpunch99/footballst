import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv() 

API_KEY = os.getenv("API_KEY")


url = "https://v3.football.api-sports.io/fixtures?league=39&season=2023"
headers = {"x-apisports-key": API_KEY}


response = requests.get(url, headers=headers)
data = response.json()

matches = data.get("response", [])


match_list = []
for match in matches:
    fixture = match['fixture']
    teams = match['teams']
    goals = match['goals']

    match_list.append({
        "match_date": fixture['date'],
        "home_team": teams['home']['name'],
        "away_team": teams['away']['name'],
        "home_goals": goals['home'],
        "away_goals": goals['away']
    })

df = pd.DataFrame(match_list)

print("데이터프레임")
print(df.head())


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)


df.to_sql("matches", engine, if_exists="append", index=False)

print("DB 저장")
