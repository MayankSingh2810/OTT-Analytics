from pyspark.sql.functions import *


def build_device_analytics(spark):

    df = spark.read.parquet("data_lake/silver/watch_history")

    device = (
        df.groupBy("device")
        .agg(
            count("*").alias("views"),
            avg("watch_seconds").alias("avg_watch_seconds"),
            avg("completion_pct").alias("completion"),
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