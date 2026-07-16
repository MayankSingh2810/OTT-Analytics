"""
============================================================
OTT STREAM INTELLIGENCE PLATFORM
Gold Layer -> MySQL Loader
============================================================
"""

from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "1234"          # <-- Change if your MySQL password is different
MYSQL_DATABASE = "ott_analytics"

DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

engine = create_engine(DATABASE_URL)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

GOLD_PATH = PROJECT_ROOT / "data_lake" / "gold"

TABLES = [
    "dashboard_summary",
    "daily_active_users",
    "monthly_active_users",
    "user_retention",
    "top_content",
    "content_performance",
    "genre_analytics",
    "country_stats",
    "device_stats",
    "hourly_usage",
    "quality_stats",
    "subscription_revenue",
    "watch_time_summary",
    "churn_features",
]


def load_gold_tables():

    print("=" * 80)
    print("LOADING GOLD TABLES TO MYSQL")
    print("=" * 80)

    for table in TABLES:

        folder = GOLD_PATH / table

        if not folder.exists():
            print(f"Skipping {table} (folder not found)")
            continue

        print(f"\nLoading {table}")

        df = pd.read_parquet(folder)

        df.to_sql(
            table,
            engine,
            if_exists="replace",
            index=False
        )

        print(f"✓ {table} ({len(df):,} rows)")

    print("\n")
    print("=" * 80)
    print("ALL GOLD TABLES LOADED")
    print("=" * 80)


if __name__ == "__main__":
    load_gold_tables()