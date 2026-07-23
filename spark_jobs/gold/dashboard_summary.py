"""
==========================================================
Gold Layer
LIVE Dashboard Summary
(Historical + Live)
==========================================================
"""

from pyspark.sql.functions import (
    count,
    countDistinct,
    sum,
    avg,
    when,
    col,
)

import builtins

from config import GOLD_DIR
from spark_jobs.gold.load_all_users import load_all_users


def build_dashboard_summary(spark):

    print("=" * 70)
    print("Building LIVE Dashboard Summary")
    print("=" * 70)

    # ======================================================
    # Historical Watch History
    # ======================================================

    watch = spark.read.parquet(
        "data_lake/silver/watch_history"
    )

    # ======================================================
    # Live Events
    # ======================================================

    try:

        live = spark.read.parquet(
            "data_lake/silver/live_events"
        )

        live = (
            live
            .withColumn("watch_id", col("event_id"))
            .withColumn("watch_start", col("timestamp"))
            .withColumn("watch_end", col("timestamp"))
            .withColumn("watch_minutes", col("watch_seconds") / 60)

            .withColumn(
                "liked",
                when(col("event_type") == "LIKE", "Yes").otherwise("No")
            )

            .withColumn(
                "added_to_watchlist",
                when(col("event_type") == "ADD_TO_WATCHLIST", "Yes").otherwise("No")
            )

            .withColumn(
                "completed",
                when(col("completion_pct") >= 90, "Yes").otherwise("No")
            )

            .withColumn(
                "recommendation_source",
                when(col("event_type") == "RECOMMENDATION", "Recommended").otherwise("Direct")
            )

            .withColumn("engagement_level", col("event_type"))

            .withColumn(
                "binge_watch",
                when(col("watch_seconds") >= 7200, "Yes").otherwise("No")
            )

            .select(watch.columns)
        )

        all_watch = watch.unionByName(
            live,
            allowMissingColumns=True
        )

    except Exception:

        print("No live events found.")

        all_watch = watch

    # ======================================================
    # Combined Users
    # ======================================================

    users = load_all_users(spark)

    # ======================================================
    # Metrics
    # ======================================================

    metrics = (

        all_watch

        .agg(

            count("*").alias("total_events"),

            countDistinct("user_id").alias("unique_users"),

            countDistinct("content_id").alias("unique_content"),

            sum("watch_minutes").alias("total_watch_minutes"),

            avg("watch_minutes").alias("avg_watch_minutes"),

            avg("completion_pct").alias("avg_completion"),

            avg(
                when(col("liked") == "Yes", 1).otherwise(0)
            ).alias("like_rate"),

            avg(
                when(col("completed") == "Yes", 1).otherwise(0)
            ).alias("completion_rate"),

            avg(
                when(col("binge_watch") == "Yes", 1).otherwise(0)
            ).alias("binge_watch_rate")

        )

    ).collect()[0]

    registered_users = users.count()

    summary = spark.createDataFrame(

        [(
            int(metrics["total_events"]),

            int(metrics["unique_users"]),

            int(metrics["unique_content"]),

            builtins.round(
                metrics["total_watch_minutes"] / 60,
                2
            ),

            builtins.round(
                metrics["avg_watch_minutes"],
                2
            ),

            builtins.round(
                metrics["avg_completion"],
                2
            ),

            builtins.round(
                metrics["like_rate"],
                2
            ),

            builtins.round(
                metrics["completion_rate"],
                2
            ),

            builtins.round(
                metrics["binge_watch_rate"],
                2
            ),

            int(metrics["unique_content"]),

            registered_users

        )],

        [
            "total_events",
            "unique_users",
            "unique_content",
            "watch_hours",
            "avg_watch_minutes",
            "avg_completion",
            "like_rate",
            "completion_rate",
            "binge_watch_rate",
            "content_library",
            "registered_users",
        ]

    )

    output = GOLD_DIR / "dashboard_summary"

    summary.write.mode("overwrite").parquet(
        str(output)
    )

    print(f"Rows : {summary.count():,}")
    print(f"Saved : {output}")

    return summary