from pathlib import Path

from pyspark.sql import SparkSession
from sqlalchemy import create_engine
import os

# ============================================================
# Spark Session
# ============================================================

spark = (
    SparkSession.builder
    .appName("OTT Enterprise Gold Loader")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

print("=" * 80)
print("        OTT ENTERPRISE GOLD -> MYSQL ETL")
print("=" * 80)

# ============================================================
# MySQL Configuration
# ============================================================

MYSQL_USER = "root"
MYSQL_PASSWORD = "1234"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "ott_analytics"

engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

# ============================================================
# Gold Layer Location
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

GOLD_DIR = PROJECT_ROOT / "data_lake" / "gold"

print(f"\nGold Directory : {GOLD_DIR}")

# ============================================================
# Discover Gold Tables Automatically
# ============================================================

gold_tables = sorted(
    [
        folder.name
        for folder in GOLD_DIR.iterdir()
        if folder.is_dir()
    ]
)

print(f"\nDiscovered {len(gold_tables)} Gold tables.\n")

loaded = 0
failed = 0

# ============================================================
# Load Every Table
# ============================================================

for table in gold_tables:

    try:

        print("-" * 70)
        print(f"Loading : {table}")

        parquet_path = GOLD_DIR / table

        spark_df = spark.read.parquet(str(parquet_path))

        pandas_df = spark_df.toPandas()

        pandas_df.to_sql(
            table,
            engine,
            if_exists="replace",
            index=False,
            chunksize=5000,
            method="multi"
        )

        print(f"SUCCESS : {table}")
        print(f"Rows     : {len(pandas_df)}")

        loaded += 1

    except Exception as e:

        failed += 1

        print(f"FAILED : {table}")
        print(e)

print("\n")
print("=" * 80)
print("ETL FINISHED")
print("=" * 80)
print(f"Tables Loaded : {loaded}")
print(f"Tables Failed : {failed}")
print("=" * 80)

spark.stop()