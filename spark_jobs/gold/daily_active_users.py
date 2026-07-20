"""
==========================================================
Gold Layer
Daily Active Users
(Historical + Live)
==========================================================
"""

from pyspark.sql.functions import (
    to_date,
    to_timestamp,
    countDistinct,
    count,
    avg,
    round,
    col,
    lit,
    when
)

from config import SILVER_DIR, GOLD_DIR


def build_daily_active_users(spark):

    print("=" * 70)
    print("Building Daily Active Users")
    print("=" * 70)

    # =====================================================
    # Historical Watch History
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

    # =====================================================
    # Convert Live -> Watch Schema
    # =====================================================

    live = (

        live

        .withColumn("watch_id", col("event_id"))

        .withColumn("watch_start", col("timestamp"))

        .withColumn("watch_end", col("timestamp"))

        .withColumn(
            "watch_minutes",
            round(col("watch_seconds") / 60, 2)
        )

        .withColumn(
            "liked",
            when(col("event_type") == "LIKE", "Yes")
            .otherwise("No")
        )

        .withColumn(
            "added_to_watchlist",
            lit("No")
        )

        .withColumn(
            "completed",
            when(col("completion_pct") >= 90, "Yes")
            .otherwise("No")
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
            when(col("watch_seconds") >= 7200, "Yes")
            .otherwise("No")
        )

        .select(watch.columns)

    )

    # =====================================================
    # Merge Historical + Live
    # =====================================================

    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    # =====================================================
    # Daily KPIs
    # =====================================================

    daily = (

        all_watch

        .withColumn(
            "event_date",
            to_date(to_timestamp("watch_start"))
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
            ).alias("avg_watch_minutes")

        )

        .orderBy("event_date")

    )

    # =====================================================
    # Save
    # =====================================================

    output = GOLD_DIR / "daily_active_users"

    (
        daily.write
        .mode("overwrite")
        .parquet(str(output))
    )

    print(f"Rows : {daily.count():,}")
    print(f"Saved : {output}")

    return daily