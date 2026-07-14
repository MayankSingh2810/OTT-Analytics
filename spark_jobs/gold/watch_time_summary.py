"""
==========================================================
Gold Layer
Watch Time Summary
Enterprise Version
==========================================================
"""

from pyspark.sql.functions import (
    sum,
    avg,
    round,
    count,
    countDistinct,
    when,
    col
)

from config import SILVER_DIR, GOLD_DIR


def build_watch_time_summary(spark):

    print("=" * 70)
    print("Building Watch Time Summary")
    print("=" * 70)

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    summary = (

        watch

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