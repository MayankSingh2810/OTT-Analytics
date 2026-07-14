"""
==========================================================
Gold Layer
Hourly Usage
Enterprise Version
==========================================================
"""

from pyspark.sql.functions import (
    hour,
    col,
    count,
    avg,
    round,
    sum
)

from config import SILVER_DIR, GOLD_DIR


def build_hourly_usage(spark):

    print("=" * 70)
    print("Building Hourly Usage")
    print("=" * 70)

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    hourly = (

        watch

        .withColumn(
            "hour",
            hour(col("watch_start"))
        )

        .groupBy("hour")

        .agg(

            count("*").alias("events"),

            round(
                avg("watch_minutes"),
                2
            ).alias("avg_watch_minutes"),

            round(
                sum("watch_minutes") / 60,
                2
            ).alias("watch_hours"),

            round(
                avg("completion_pct"),
                2
            ).alias("avg_completion")

        )

        .orderBy("hour")

    )

    output = GOLD_DIR / "hourly_usage"

    hourly.write.mode("overwrite").parquet(
        str(output)
    )

    print(f"Rows : {hourly.count():,}")
    print(f"Saved : {output}")

    return hourly