"""
============================================================
OTT STREAM INTELLIGENCE PLATFORM
Database Seeder
============================================================
"""

import pandas as pd
from sqlalchemy import create_engine

from config import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
    RAW_DATA_DIR,
)

from database.csv_loader import CSVLoader


# ==========================================================
# MYSQL CONNECTION
# ==========================================================

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


# ==========================================================
# TABLE LOAD ORDER
# ==========================================================

TABLES = [
    "subscription_plans",
    "users",
    "content",
    "subscriptions",
    "user_behavior",
    "watch_history",
    "ratings",
    "search_history",
    "sessions",
]


# ==========================================================
# LOAD TABLES
# ==========================================================

for table in TABLES:

    print("=" * 80)
    print(f"Loading Table : {table}")
    print("=" * 80)

    loader = CSVLoader(
        RAW_DATA_DIR / f"{table}.csv"
    )

    df = loader.load()

    loader.validate(df)

    print(f"Inserting {len(df):,} rows...")

    df.to_sql(
        table,
        engine,
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi",
    )

    print(f"✓ {table} Loaded Successfully\n")


print("=" * 80)
print("DATABASE LOADING COMPLETED")
print("=" * 80)