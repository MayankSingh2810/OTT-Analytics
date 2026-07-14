"""
============================================================
Gold Layer
Churn Features
============================================================
"""

from pyspark.sql.functions import (
    count,
    sum,
    avg,
    round,
    datediff,
    current_date,
    max,
    when
)

from config import SILVER_DIR, GOLD_DIR


def build_churn_features(spark):

    print("=" * 70)
    print("Building Churn Features")
    print("=" * 70)

    # ======================================================
    # Read Silver Tables
    # ======================================================

    users = spark.read.parquet(
        str(SILVER_DIR / "users")
    )

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    # ======================================================
    # Aggregate Watch History
    # ======================================================

    watch_summary = (

        watch

        .groupBy("user_id")

        .agg(

            count("*").alias("total_views"),

            round(
                sum("watch_minutes"),
                2
            ).alias("total_watch_minutes"),

            round(
                avg("completion_pct"),
                2
            ).alias("avg_completion"),

            max("watch_start").alias("last_watch")

        )

    )

    # ======================================================
    # LEFT JOIN WITH USERS
    # Keeps every registered user
    # ======================================================

    churn = (

        users

        .select("user_id")

        .join(
            watch_summary,
            on="user_id",
            how="left"
        )

    )

    # ======================================================
    # Replace Nulls
    # ======================================================

    churn = churn.fillna({

        "total_views": 0,

        "total_watch_minutes": 0,

        "avg_completion": 0

    })

    # ======================================================
    # Days Since Last Watch
    # ======================================================

    churn = churn.withColumn(

        "days_inactive",

        when(

            churn.last_watch.isNull(),

            None

        ).otherwise(

            datediff(
                current_date(),
                churn.last_watch
            )

        )

    )

    # ======================================================
    # Churn Label
    # ======================================================

    churn = churn.withColumn(

        "churn_label",

        when(

            churn.last_watch.isNull(),

            1

        ).when(

            churn.days_inactive > 60,

            1

        ).otherwise(

            0

        )

    )

    # ======================================================
    # Save
    # ======================================================

    output = GOLD_DIR / "churn_features"

    churn.write.mode("overwrite").parquet(str(output))

    print(f"Rows : {churn.count():,}")

    print(f"Saved : {output}")

    return churn