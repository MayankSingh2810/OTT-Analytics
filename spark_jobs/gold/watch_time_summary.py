"""
==========================================================
Gold Layer
Watch Time Summary
LIVE + Historical
==========================================================
"""

from pyspark.sql.functions import (
    sum,
    avg,
    round,
    count,
    countDistinct,
    when,
    col,
    lit
)

from config import SILVER_DIR, GOLD_DIR


def build_watch_time_summary(spark):

    print("=" * 70)
    print("Building Watch Time Summary")
    print("=" * 70)

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    live = spark.read.parquet(
        str(SILVER_DIR / "live_events")
    )

    # Convert live events into watch_history schema
    live = (

        live

        .withColumn(
            "watch_id",
            col("event_id")
        )

        .withColumn(
            "watch_start",
            col("timestamp")
        )

        .withColumn(
            "watch_end",
            col("timestamp")
        )

        .withColumn(
            "watch_minutes",
            round(col("watch_seconds") / 60, 2)
        )

        .withColumn(
            "completed",
            when(col("completion_pct") >= 90, "Yes")
            .otherwise("No")
        )

        .withColumn(
            "liked",
            lit("No")
        )

        .withColumn(
            "added_to_watchlist",
            lit("No")
        )

        .withColumn(
            "recommendation_source",
            lit("Live")
        )

        .withColumn(
            "engagement_level",
            lit("Live")
        )

        .withColumn(
            "binge_watch",
            lit("No")
        )

        .select(watch.columns)

    )

    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    summary = (

        all_watch

        .agg(

            count("*").alias("total_events"),

            countDistinct("user_id").alias("unique_users"),

            countDistinct("content_id").alias("unique_content"),

            round(
                sum("watch_minutes") / 60,
                2
            ).alias("total_watch_hours"),

            round(
                avg("watch_minutes"),
                2
            ).alias("avg_watch_minutes"),

            round(
                avg("completion_pct"),
                2
            ).alias("avg_completion"),

            round(
                avg(
                    when(col("liked") == "Yes", 1).otherwise(0)
                ),
                2
            ).alias("like_rate"),

            round(
                avg(
                    when(col("completed") == "Yes", 1).otherwise(0)
                ),
                2
            ).alias("completion_rate"),

            round(
                avg(
                    when(col("binge_watch") == "Yes", 1).otherwise(0)
                ),
                2
            ).alias("binge_watch_rate")

        )

    )

    output = GOLD_DIR / "watch_time_summary"

    summary.write.mode("overwrite").parquet(
        str(output)
    )

    print(f"Rows : {summary.count():,}")
    print(f"Saved : {output}")

    return summary