"""
============================================================
Silver Layer
Watch History
============================================================
"""

from pyspark.sql.functions import (
    col,
    when,
    round
)

from config import BRONZE_DIR, SILVER_DIR


def transform_watch_history(spark):

    print("=" * 70)
    print("Processing Watch History")
    print("=" * 70)

    df = spark.read.parquet(
        str(BRONZE_DIR / "watch_history")
    )

    print(f"Original Rows : {df.count():,}")

    df = df.dropDuplicates(["watch_id"])

    df = df.filter(col("watch_minutes") > 0)

    df = df.withColumn(
        "completion_pct",
        round(col("completion_pct"), 2)
    )

    df = df.withColumn(

        "completed",

        when(col("completion_pct") >= 90, "Yes")
        .otherwise("No")

    )

    df = df.withColumn(

        "engagement_level",

        when(col("completion_pct") >= 90, "High")
        .when(col("completion_pct") >= 60, "Medium")
        .otherwise("Low")

    )

    df = df.withColumn(

        "binge_watch",

        when(col("watch_minutes") >= 120, "Yes")
        .otherwise("No")

    )

    output = SILVER_DIR / "watch_history"

    df.write.mode("overwrite").parquet(str(output))

    print(f"Saved : {output}")

    return df