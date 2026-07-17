"""
==========================================================
Gold Layer
LIVE Dashboard Summary
(Historical + Streaming)
==========================================================
"""

from pyspark.sql.functions import (
    count,
    countDistinct,
    sum,
    avg,
    lit,
    when,
    col
)

import builtins

from config import GOLD_DIR


def build_dashboard_summary(spark):

    print("=" * 70)
    print("Building LIVE Dashboard Summary")
    print("=" * 70)

    # ======================================================
    # Historical Dataset
    # ======================================================

    watch = spark.read.parquet(
        "data_lake/silver/watch_history"
    )

    # ======================================================
    # Streaming Dataset
    # ======================================================

    live = spark.read.parquet(
        "data_lake/silver/live_events"
    )

    # ======================================================
    # Historical Metrics
    # ======================================================

    hist = (

        watch

        .agg(

            count("*").alias("hist_events"),

            countDistinct("user_id").alias("hist_users"),

            countDistinct("content_id").alias("hist_content"),

            sum("watch_minutes").alias("hist_minutes"),

            avg("watch_minutes").alias("hist_avg_minutes"),

            avg("completion_pct").alias("hist_completion"),

            avg(
                when(col("liked") == "Yes", 1).otherwise(0)
            ).alias("hist_like"),

            avg(
                when(col("completed") == "Yes", 1).otherwise(0)
            ).alias("hist_completed"),

            avg(
                when(col("binge_watch") == "Yes", 1).otherwise(0)
            ).alias("hist_binge")

        )

    ).collect()[0]

    # ======================================================
    # Live Metrics
    # ======================================================

    live_metrics = (

        live

        .agg(

            count("*").alias("live_events"),

            countDistinct("user_id").alias("live_users"),

            countDistinct("content_id").alias("live_content"),

            sum("watch_seconds").alias("live_seconds"),

            avg("watch_seconds").alias("live_avg_seconds"),

            avg("completion_pct").alias("live_completion"),

            avg(
                when(col("event_type") == "LIKE", 1).otherwise(0)
            ).alias("live_like"),

            avg(
                when(col("completion_pct") >= 90, 1).otherwise(0)
            ).alias("live_completed"),

            avg(
                when(col("watch_seconds") >= 7200, 1).otherwise(0)
            ).alias("live_binge")

        )

    ).collect()[0]

    # ======================================================
    # Merge Historical + Live
    # ======================================================

    total_events = hist["hist_events"] + live_metrics["live_events"]

    total_watch_hours = (
        hist["hist_minutes"] / 60
    ) + (
        live_metrics["live_seconds"] / 3600
    )

    avg_watch_minutes = (
        hist["hist_avg_minutes"] +
        (live_metrics["live_avg_seconds"] / 60)
    ) / 2

    avg_completion = (
        hist["hist_completion"] +
        live_metrics["live_completion"]
    ) / 2

    like_rate = (
        hist["hist_like"] +
        live_metrics["live_like"]
    ) / 2

    completion_rate = (
        hist["hist_completed"] +
        live_metrics["live_completed"]
    ) / 2

    binge_rate = (
        hist["hist_binge"] +
        live_metrics["live_binge"]
    ) / 2

    summary = spark.createDataFrame(

        [(
            int(total_events),

            int(max(
                hist["hist_users"],
                live_metrics["live_users"]
            )),

            int(max(
                hist["hist_content"],
                live_metrics["live_content"]
            )),

            builtins.round(total_watch_hours, 2),

            builtins.round(avg_watch_minutes, 2),

            builtins.round(avg_completion, 2),

            builtins.round(like_rate, 2),

            builtins.round(completion_rate, 2),

            builtins.round(binge_rate, 2),

            5000,

            100000
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
            "registered_users"
        ]

    )

    output = GOLD_DIR / "dashboard_summary"

    summary.write.mode("overwrite").parquet(str(output))

    print(f"Rows : {summary.count():,}")
    print(f"Saved : {output}")

    return summary