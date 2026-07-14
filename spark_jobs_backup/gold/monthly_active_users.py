"""
============================================================
Gold Layer
Monthly Active Users
============================================================
"""

from pyspark.sql.functions import (
    col,
    date_format,
    countDistinct
)

from config import SILVER_DIR, GOLD_DIR


def build_monthly_active_users(spark):

    print("=" * 70)
    print("Building Monthly Active Users")
    print("=" * 70)

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    mau = (

        watch

        .withColumn(
            "month",
            date_format(col("watch_start"), "yyyy-MM")
        )

        .groupBy("month")

        .agg(
            countDistinct("user_id")
            .alias("monthly_active_users")
        )

        .orderBy("month")

    )

    output = GOLD_DIR / "monthly_active_users"

    mau.write.mode("overwrite").parquet(str(output))

    print(f"Rows : {mau.count():,}")
    print(f"Saved : {output}")

    return mau