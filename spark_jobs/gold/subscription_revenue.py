"""
==========================================================
Gold Layer
Subscription Revenue
Enterprise Version
==========================================================
"""

from pyspark.sql.functions import (
    count,
    sum,
    avg,
    round,
    when,
    col
)

from config import SILVER_DIR, GOLD_DIR


def build_subscription_revenue(spark):

    print("=" * 70)
    print("Building Subscription Revenue")
    print("=" * 70)

    subscriptions = spark.read.parquet(
        str(SILVER_DIR / "subscriptions")
    )

    revenue = (

        subscriptions

        .agg(

            count("*").alias("total_subscribers"),

            sum(
                when(
                    col("subscription_status") == "Active",
                    1
                ).otherwise(0)
            ).alias("active_subscribers"),

            sum(
                when(
                    col("auto_renew") == "Yes",
                    1
                ).otherwise(0)
            ).alias("auto_renew_users"),

            round(
                avg("monthly_price"),
                2
            ).alias("average_plan_price"),

            round(
                sum("monthly_price"),
                2
            ).alias("monthly_revenue")

        )

    )

    output = GOLD_DIR / "subscription_revenue"

    revenue.write.mode("overwrite").parquet(
        str(output)
    )

    print(f"Rows : {revenue.count():,}")
    print(f"Saved : {output}")

    return revenue