from pyspark.sql.functions import (
    date_format,
    countDistinct,
    count,
    avg,
    sum,
    round,
    col,
    lit,
    when
)

from config import SILVER_DIR, GOLD_DIR


def build_monthly_active_users(spark):

    print("=" * 70)
    print("Building Monthly Active Users")
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
    # Convert Live -> Watch History Schema
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
    # Merge Historical + Live Events
    # =====================================================

    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    # =====================================================
    # Monthly KPIs
    # =====================================================

    monthly = (

        all_watch

        .withColumn(
            "month",
            date_format(col("watch_start"), "yyyy-MM")
        )

        .groupBy("month")

        .agg(

            countDistinct("user_id")
                .alias("monthly_active_users"),

            count("*")
                .alias("total_events"),

            round(
                sum("watch_minutes") / 60,
                2
            ).alias("watch_hours"),

            round(
                avg("watch_minutes"),
                2
            ).alias("avg_watch_minutes"),

            round(
                avg("completion_pct"),
                2
            ).alias("avg_completion")

        )

        .orderBy("month")

    )

    # =====================================================
    # Save
    # =====================================================

    output = GOLD_DIR / "monthly_active_users"

    (
        monthly.write
        .mode("overwrite")
        .parquet(str(output))
    )

    print(f"Rows : {monthly.count():,}")
    print(f"Saved : {output}")

    return monthly