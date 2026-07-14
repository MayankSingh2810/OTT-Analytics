"""
============================================================
Silver Layer - Sessions
============================================================
"""

from pyspark.sql.functions import (
    col,
    when,
    hour
)

from config import BRONZE_DIR, SILVER_DIR


def transform_sessions(spark):

    print("=" * 70)
    print("Processing Sessions")
    print("=" * 70)

    df = spark.read.parquet(
        str(BRONZE_DIR / "sessions")
    )

    print(f"Original Rows : {df.count():,}")

    # -------------------------------------------------------
    # Remove duplicate sessions
    # -------------------------------------------------------

    df = df.dropDuplicates(["session_id"])

    # -------------------------------------------------------
    # Keep only valid session durations
    # -------------------------------------------------------

    df = df.filter(
        col("session_minutes") > 0
    )

    # -------------------------------------------------------
    # Login Hour
    # -------------------------------------------------------

    df = df.withColumn(
        "login_hour",
        hour("login_time")
    )

    # -------------------------------------------------------
    # Time of Day
    # -------------------------------------------------------

    df = df.withColumn(

        "time_of_day",

        when(col("login_hour") < 6, "Night")
        .when(col("login_hour") < 12, "Morning")
        .when(col("login_hour") < 18, "Afternoon")
        .otherwise("Evening")

    )

    # -------------------------------------------------------
    # Session Category
    # -------------------------------------------------------

    df = df.withColumn(

        "session_category",

        when(col("session_minutes") < 15, "Short")
        .when(col("session_minutes") < 60, "Medium")
        .otherwise("Long")

    )

    print(f"Final Rows : {df.count():,}")

    output = SILVER_DIR / "sessions"

    df.write.mode("overwrite").parquet(str(output))

    print(f"Saved : {output}")

    return df