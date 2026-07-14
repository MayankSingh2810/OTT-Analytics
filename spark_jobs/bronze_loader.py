"""
============================================================
Enterprise Bronze Loader
CSV → Bronze Parquet
============================================================
"""

from pathlib import Path

from config import RAW_DATA_DIR, BRONZE_DIR
from spark_jobs.spark_session import create_spark_session

spark = create_spark_session()

TABLES = [
    "users",
    "content",
    "subscriptions",
    "subscription_plans",
    "watch_history",
    "ratings",
    "search_history",
    "sessions",
    "user_behavior",
]

print("=" * 80)
print("BUILDING BRONZE LAYER")
print("=" * 80)

for table in TABLES:

    csv_path = RAW_DATA_DIR / f"{table}.csv"

    if not csv_path.exists():
        print(f"Skipping {table} (CSV not found)")
        continue

    print(f"\nLoading {table}")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(str(csv_path))
    )

    print(f"Rows : {df.count():,}")

    output = BRONZE_DIR / table

    (
        df.write
        .mode("overwrite")
        .parquet(str(output))
    )

    print(f"Saved -> {output}")

spark.stop()

print("\n" + "=" * 80)
print("Bronze Layer Created Successfully")
print("=" * 80)