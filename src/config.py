import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

# Supabase PostgreSQL Connection String
DB_HOST = os.getenv("DB_HOST", "db.YOUR_PROJECT_REF.supabase.co")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

# Construct SQLAlchemy Database URL
# Uses psycopg2 driver implicitly when starting with postgresql://
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_engine():
    """Returns a SQLAlchemy engine instance for the Supabase DB."""
    return create_engine(DATABASE_URL)
