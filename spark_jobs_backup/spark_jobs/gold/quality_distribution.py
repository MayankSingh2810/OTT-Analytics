from pyspark.sql.functions import *


def build_quality_distribution(spark):

    df = spark.read.parquet("data_lake/silver/watch_history")

    quality = (
        df.groupBy("quality")
        .agg(
            count("*").alias("events"),
            avg("watch_seconds").alias("avg_watch_seconds"),
            avg("completion_pct").alias("completion")
        )
    )

    (
        quality.write
        .mode("overwrite")
        .parquet("data_lake/gold/quality_distribution")
    )

    print("✓ quality_distribution")