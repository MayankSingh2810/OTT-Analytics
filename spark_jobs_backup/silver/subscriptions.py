"""
============================================================
Silver Layer - Subscriptions
============================================================
"""

from pyspark.sql.functions import (
    col,
    when,
    datediff,
    current_date
)

from config import BRONZE_DIR, SILVER_DIR


def transform_subscriptions(spark):

    print("=" * 70)
    print("Processing Subscriptions")
    print("=" * 70)

    df = spark.read.parquet(
        str(BRONZE_DIR / "subscriptions")
    )

    print(f"Original Rows : {df.count():,}")

    # -------------------------------------------------------
    # Remove duplicates
    # -------------------------------------------------------

    df = df.dropDuplicates(["subscription_id"])

    # -------------------------------------------------------
    # Days until renewal
    # -------------------------------------------------------

    df = df.withColumn(

        "days_to_renewal",

        datediff(
            col("renewal_date"),
            current_date()
        )

    )

    # -------------------------------------------------------
    # Renewal Status
    # -------------------------------------------------------

    df = df.withColumn(

        "renewal_status",

        when(col("days_to_renewal") <= 7, "Renew Soon")
        .when(col("days_to_renewal") <= 30, "Upcoming")
        .otherwise("Active")

    )

    print(f"Final Rows : {df.count():,}")

    output = SILVER_DIR / "subscriptions"

    df.write.mode("overwrite").parquet(str(output))

    print(f"Saved : {output}")

    return df