import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "footballst")

DB_URL = (
    f"postgresql+psycopg2://{DB_USER}:"
    f"{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

API_BASE_URL = "https://v3.football.api-sports.io"
