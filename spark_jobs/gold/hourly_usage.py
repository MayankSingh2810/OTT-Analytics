"""
==========================================================
Gold Layer
Hourly Usage
LIVE + Historical
==========================================================
"""

from pyspark.sql.functions import (
    hour,
    col,
    count,
    avg,
    round,
    sum,
    to_timestamp
)

from config import SILVER_DIR, GOLD_DIR


def build_hourly_usage(spark):

    print("=" * 70)
    print("Building Hourly Usage")
    print("=" * 70)

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    live = spark.read.parquet(
        str(SILVER_DIR / "live_events")
    )

    live = (
        live
        .withColumn(
            "watch_minutes",
            col("watch_seconds") / 60
        )
        .withColumn(
            "watch_start",
            to_timestamp(col("timestamp"))
        )
    )

    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    hourly = (

        all_watch

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