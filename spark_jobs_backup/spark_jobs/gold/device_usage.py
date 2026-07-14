"""
============================================================
Gold Layer
Device Usage Analytics
============================================================
"""

from pyspark.sql.functions import (
    count,
    round,
    sum,
    col
)

from config import SILVER_DIR, GOLD_DIR


def build_device_usage(spark):

    print("=" * 70)
    print("Building Device Usage")
    print("=" * 70)

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    device = (

        watch

        .groupBy("device")

        .agg(
            count("*").alias("total_views")
        )

    )

    total_views = device.agg(
        sum("total_views").alias("total")
    ).collect()[0]["total"]

    device = device.withColumn(

        "usage_percent",

        round(
            (col("total_views") / total_views) * 100,
            2
        )

    ).orderBy(col("total_views").desc())

    output = GOLD_DIR / "device_usage"

    device.write.mode("overwrite").parquet(str(output))

    print(f"Rows : {device.count():,}")

    print(f"Saved : {output}")

    return device