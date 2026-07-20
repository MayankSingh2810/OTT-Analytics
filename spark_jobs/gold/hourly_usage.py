"""
==========================================================
Gold Layer
Hourly Usage
(Historical + Live Events)
==========================================================
"""

from pyspark.sql.functions import (
    hour,
    col,
    count,
    avg,
    round,
    sum,
    to_timestamp,
    when,
    lit
)

from config import SILVER_DIR, GOLD_DIR


def build_hourly_usage(spark):

    print("=" * 70)
    print("Building Hourly Usage")
    print("=" * 70)

    # =====================================================
    # Historical
    # =====================================================

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    # =====================================================
    # Live Events
    # =====================================================

    live = spark.read.parquet(
        str(SILVER_DIR / "live_events")
    )

    live = (
        live
        .withColumn("watch_id", col("event_id"))
        .withColumn("watch_start", to_timestamp(col("timestamp")))
        .withColumn("watch_end", to_timestamp(col("timestamp")))
        .withColumn(
            "watch_minutes",
            round(col("watch_seconds") / 60, 2)
        )
        .withColumn(
            "liked",
            when(col("event_type") == "LIKE", "Yes").otherwise("No")
        )
        .withColumn("added_to_watchlist", lit("No"))
        .withColumn(
            "completed",
            when(col("completion_pct") >= 90, "Yes").otherwise("No")
        )
        .withColumn("recommendation_source", lit("Live"))
        .withColumn("engagement_level", lit("Live"))
        .withColumn(
            "binge_watch",
            when(col("watch_seconds") >= 7200, "Yes").otherwise("No")
        )
        .select(watch.columns)
    )

    # =====================================================
    # Historical + Live
    # =====================================================

    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    # =====================================================
    # Hourly Usage
    # =====================================================

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