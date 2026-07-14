from pyspark.sql.functions import *


def build_country_analytics(spark):

    df = spark.read.parquet("data_lake/silver/watch_history")

    country = (
        df.groupBy("country")
        .agg(
            count("*").alias("views"),
            avg("watch_seconds").alias("avg_watch_seconds"),
            avg("completion_pct").alias("avg_completion"),
            countDistinct("user_id").alias("unique_users")
        )
        .orderBy(desc("views"))
    )

    (
        country.write
        .mode("overwrite")
        .parquet("data_lake/gold/country_analytics")
    )

    print("✓ country_analytics")