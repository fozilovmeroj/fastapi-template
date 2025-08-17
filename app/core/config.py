import os

from dotenv import load_dotenv

load_dotenv()

DEBUG: bool = os.getenv("DEBUG") == "True"
DATABASE_URL: str = os.getenv("DATABASE_URL", default="sqlite:///app.db")
ALEMBIC_DATABASE_URL: str = os.getenv(
    "ALEMBIC_DATABASE_URL", default="sqlite:///app.db"
)
LOCALE: str = os.getenv("LOCALE", default="en")
