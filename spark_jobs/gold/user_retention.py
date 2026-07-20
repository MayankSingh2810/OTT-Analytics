from pyspark.sql.functions import (
    count,
    avg,
    max,
    min,
    datediff,
    current_date,
    round,
    when,
    col,
    lit
)

from config import SILVER_DIR, GOLD_DIR


def build_user_retention(spark):

    print("=" * 70)
    print("Building User Retention")
    print("=" * 70)

    # =====================================================
    # Historical
    # =====================================================

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    users = spark.read.parquet(
        str(SILVER_DIR / "users")
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
        .withColumn("watch_start", col("timestamp"))
        .withColumn("watch_end", col("timestamp"))
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
    # Retention Features
    # =====================================================

    retention = (

        all_watch

        .groupBy("user_id")

        .agg(

            count("*").alias("total_sessions"),

            round(
                avg("watch_minutes"),
                2
            ).alias("avg_watch_minutes"),

            round(
                avg("completion_pct"),
                2
            ).alias("avg_completion"),

            max("watch_start").alias("last_activity"),

            min("watch_start").alias("first_activity")

        )

        .withColumn(
            "days_inactive",
            datediff(
                current_date(),
                col("last_activity")
            )
        )

        .withColumn(
            "user_status",
            when(
                col("days_inactive") <= 30,
                "Active"
            ).otherwise("Inactive")
        )

        .join(
            users,
            "user_id",
            "left"
        )

    )

    output = GOLD_DIR / "user_retention"

    retention.write.mode("overwrite").parquet(
        str(output)
    )

    print(f"Rows : {retention.count():,}")
    print(f"Saved : {output}")

    return retention