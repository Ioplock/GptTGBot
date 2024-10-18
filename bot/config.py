import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SQL_FILE = os.getenv("SQL_FILE")

DATABASE_URL = "sqlite:///database.db"