"""
==========================================================
Gold Layer
Enterprise Churn Feature Store
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
    col
)

from config import SILVER_DIR, GOLD_DIR


def build_churn_features(spark):

    print("=" * 70)
    print("Building Enterprise Churn Features")
    print("=" * 70)

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    users = spark.read.parquet(
        str(SILVER_DIR / "users")
    )

    subscriptions = spark.read.parquet(
        str(SILVER_DIR / "subscriptions")
    )

    features = (

        watch

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