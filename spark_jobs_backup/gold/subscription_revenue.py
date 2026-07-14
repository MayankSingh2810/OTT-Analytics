"""
============================================================
Gold Layer
Subscription Revenue
============================================================
"""

from pyspark.sql.functions import (
    sum,
    avg,
    count,
    when,
    round
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

            round(
                sum("monthly_price"),
                2
            ).alias("monthly_revenue"),

            round(
                avg("monthly_price"),
                2
            ).alias("average_plan_price"),

            count("*").alias("total_subscribers"),

            count(
                when(
                    subscriptions.subscription_status == "Active",
                    True
                )
            ).alias("active_subscribers"),

            count(
                when(
                    subscriptions.auto_renew == "Yes",
                    True
                )
            ).alias("auto_renew_users")

        )

    )

    output = GOLD_DIR / "subscription_revenue"

    revenue.write.mode("overwrite").parquet(str(output))

    revenue.show(truncate=False)

    print(f"Saved : {output}")

    return revenue