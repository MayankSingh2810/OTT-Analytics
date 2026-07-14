from pyspark.sql.functions import (
    count,
    min,
    max,
    datediff,
    current_date,
    when,
    coalesce,
    lit
)

from config import SILVER_DIR, GOLD_DIR


def build_user_retention(spark):

    print("=" * 70)
    print("Building User Retention")
    print("=" * 70)

    users = spark.read.parquet(
        str(SILVER_DIR / "users")
    )

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    watch_summary = (

        watch

        .groupBy("user_id")

        .agg(

            count("*").alias("total_views"),

            min("watch_start").alias("first_watch"),

            max("watch_start").alias("last_watch")

        )

    )

    retention = (

        users

        .select("user_id")

        .join(
            watch_summary,
            "user_id",
            "left"
        )

    )

    retention = retention.fillna(

        {

            "total_views": 0

        }

    )

    retention = retention.withColumn(

        "days_since_last_watch",

        when(

            retention.last_watch.isNull(),

            None

        ).otherwise(

            datediff(
                current_date(),
                retention.last_watch
            )

        )

    )

    retention = retention.withColumn(

        "user_status",

        when(
            retention.last_watch.isNull(),
            "Never Active"
        )

        .when(
            retention.days_since_last_watch <= 30,
            "Active"
        )

        .when(
            retention.days_since_last_watch <= 90,
            "At Risk"
        )

        .otherwise(
            "Inactive"
        )

    )

    output = GOLD_DIR / "user_retention"

    retention.write.mode("overwrite").parquet(str(output))

    print(f"Rows : {retention.count():,}")

    print(f"Saved : {output}")