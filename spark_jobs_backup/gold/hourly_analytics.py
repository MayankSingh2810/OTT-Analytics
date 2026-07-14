from pyspark.sql.functions import *


def build_hourly_analytics(spark):

    df = spark.read.parquet("data_lake/silver/watch_history")

    hourly = (
        df.groupBy("hour")
        .agg(
            count("*").alias("events"),
            countDistinct("user_id").alias("users"),
            avg("watch_seconds").alias("avg_watch"),
            avg("buffer_ms").alias("avg_buffer")
        )
        .orderBy("hour")
    )

    (
        hourly.write
        .mode("overwrite")
        .parquet("data_lake/gold/hourly_analytics")
    )

    print("✓ hourly_analytics")