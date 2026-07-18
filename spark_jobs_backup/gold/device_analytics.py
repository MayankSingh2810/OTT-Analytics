from pyspark.sql.functions import *


def build_device_analytics(spark):

    watch = spark.read.parquet("data_lake/silver/watch_history")
    live = spark.read.parquet("data_lake/silver/live_events")

    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    device = (
        all_watch
        .groupBy("device")
        .agg(
            count("*").alias("views"),
            round(avg("watch_seconds"), 2).alias("avg_watch_seconds"),
            round(avg("completion_pct"), 2).alias("completion"),
            countDistinct("user_id").alias("users")
        )
        .orderBy(desc("views"))
    )

    (
        device.write
        .mode("overwrite")
        .parquet("data_lake/gold/device_analytics")
    )

    print("✓ device_analytics")