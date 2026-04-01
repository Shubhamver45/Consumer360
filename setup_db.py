import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "db.YOUR_PROJECT_REF.supabase.co")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def run_sql_file(file_path):
    print(f"Executing {file_path}...")
    with open(file_path, 'r') as f:
        sql = f.read()
    with engine.connect() as conn:
        with conn.begin():
            conn.execute(text(sql))
    print(f"Executed {file_path} successfully.")

def main():
    try:
        # 1. Create raw table
        run_sql_file("sql/01_raw_schema.sql")
        
        # 2. Upload CSV to raw table
        csv_file = "raw_transaction_logs.csv"
        if os.path.exists(csv_file):
            print(f"Uploading {csv_file} to raw_transactions table...")
            df = pd.read_csv(csv_file)
            # Use to_sql carefully. append is safe. But first let's clear it just in case.
            with engine.connect() as conn:
                with conn.begin():
                    conn.execute(text("TRUNCATE TABLE raw_transactions RESTART IDENTITY CASCADE;"))
                    
            df.to_sql('raw_transactions', engine, if_exists='append', index=False)
            print("CSV uploaded successfully!")
        else:
            print(f"Could not find {csv_file}, please run download_real_data.py first.")
            return

        # 3. Process into star schema and create views
        run_sql_file("sql/02_cleaning_and_star_schema.sql")
        run_sql_file("sql/03_analytical_queries.sql")
        
        print("Database fully set up and populated!")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
