"""
============================================================
Gold Layer
Daily Active Users
============================================================
"""

from pyspark.sql.functions import (
    to_date,
    countDistinct,
    count,
    avg,
    round,
    sum,
    col
)

from config import SILVER_DIR, GOLD_DIR


def build_daily_active_users(spark):

    print("=" * 70)
    print("Building Daily Active Users")
    print("=" * 70)

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    daily = (

        watch

        .withColumn(
            "event_date",
            to_date(col("watch_start"))
        )

        .groupBy("event_date")

        .agg(

            countDistinct("user_id")
            .alias("daily_active_users"),

            count("*")
            .alias("total_events"),

            round(
                avg("watch_minutes"),
                2
            ).alias("avg_watch_minutes"),

            round(
                avg("completion_pct"),
                2
            ).alias("avg_completion"),

            round(
                sum("watch_minutes") / 60,
                2
            ).alias("watch_hours")

        )

        .orderBy("event_date")

    )

    output = GOLD_DIR / "daily_active_users"

    daily.write.mode("overwrite").parquet(str(output))

    print(f"Rows : {daily.count():,}")
    print(f"Saved : {output}")

    return daily