"""
============================================================
Silver Layer
Subscriptions
============================================================
"""

from pyspark.sql.functions import (
    col,
    when,
    datediff,
    current_date,
    to_date,
    greatest,
    lit
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

    df = df.dropDuplicates(["subscription_id"])

    df = df.withColumn(
        "renewal_date",
        to_date(col("renewal_date"))
    )

    df = df.withColumn(
        "days_to_renewal",
        greatest(
            datediff(
                col("renewal_date"),
                current_date()
            ),
            lit(0)
        )
    )

    df = df.withColumn(

        "renewal_status",

        when(col("days_to_renewal") <= 7, "Renew Soon")
        .when(col("days_to_renewal") <= 30, "Upcoming")
        .otherwise("Active")

    )

    output = SILVER_DIR / "subscriptions"

    df.write.mode("overwrite").parquet(str(output))

    print(f"Saved : {output}")

    return df