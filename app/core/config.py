from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    JWT_SECRET = os.getenv("JWT_SECRET", "changeme")
    DB_PROVIDER = "sqlite"
    DB_NAME = "sqlite3.db"

settings = Settings()
