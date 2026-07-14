"""
==========================================================
Gold Layer
User Retention
Enterprise Version
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
    when
)

from config import SILVER_DIR, GOLD_DIR


def build_user_retention(spark):

    print("=" * 70)
    print("Building User Retention")
    print("=" * 70)

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    users = spark.read.parquet(
        str(SILVER_DIR / "users")
    )

    retention = (

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

            max("watch_start").alias("last_activity"),

            min("watch_start").alias("first_activity")

        )

        .withColumn(

            "days_inactive",

            datediff(
                current_date(),
                "last_activity"
            )

        )

        .withColumn(

            "user_status",

            when(
                datediff(
                    current_date(),
                    "last_activity"
                ) <= 30,
                "Active"
            ).otherwise(
                "Inactive"
            )

        )

    )

    retention = retention.join(
        users,
        "user_id",
        "left"
    )

    output = GOLD_DIR / "user_retention"

    retention.write.mode("overwrite").parquet(
        str(output)
    )

    print(f"Rows : {retention.count():,}")

    print(f"Saved : {output}")

    return retention