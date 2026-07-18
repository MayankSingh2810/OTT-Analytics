"""
==========================================================
Gold Layer
Enterprise Churn Feature Store
(Historical + Live)
==========================================================
"""

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


def build_churn_features(spark):

    print("=" * 70)
    print("Building Enterprise Churn Features")
    print("=" * 70)

    # Historical
    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    # Live
    live = spark.read.parquet(
        str(SILVER_DIR / "live_events")
    )

    users = spark.read.parquet(
        str(SILVER_DIR / "users")
    )

    subscriptions = spark.read.parquet(
        str(SILVER_DIR / "subscriptions")
    )

    # Convert live events into watch_history format
    live = (
        live
        .withColumn("watch_id", col("event_id"))
        .withColumn("watch_start", col("timestamp"))
        .withColumn("watch_end", col("timestamp"))
        .withColumn("watch_minutes", round(col("watch_seconds") / 60, 2))
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

    # Merge historical + live
    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    features = (

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
            ).alias("binge_watch_rate"),

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
            "churn_label",
            when(
                col("days_inactive") > 30,
                1
            ).otherwise(0)
        )

    )

    features = (

        features

        .join(
            users,
            "user_id",
            "left"
        )

        .join(
            subscriptions,
            "user_id",
            "left"
        )

    )

    output = GOLD_DIR / "churn_features"

    features.write.mode("overwrite").parquet(
        str(output)
    )

    print(f"Rows : {features.count():,}")
    print(f"Saved : {output}")

    return features