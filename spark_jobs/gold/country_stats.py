from pyspark.sql.functions import (
    avg,
    count,
    countDistinct,
    col,
    round,
    lit,
    when
)

from config import SILVER_DIR, GOLD_DIR


def build_country_stats(spark):

    print("=" * 70)
    print("Building Country Statistics")
    print("=" * 70)

    # =====================================================
    # Historical
    # =====================================================

    watch = spark.read.parquet(str(SILVER_DIR / "watch_history"))
    users = spark.read.parquet(str(SILVER_DIR / "users"))
    content = spark.read.parquet(str(SILVER_DIR / "content"))

    # =====================================================
    # Live Events
    # =====================================================

    live = spark.read.parquet(str(SILVER_DIR / "live_events"))

    live = (
        live
        .withColumn("watch_id", col("event_id"))
        .withColumn("watch_start", col("timestamp"))
        .withColumn("watch_end", col("timestamp"))
        .withColumn("watch_minutes", round(col("watch_seconds") / 60, 2))
        .withColumn(
            "liked",
            when(col("event_type") == "LIKE", "Yes").otherwise("No")
        )
        .withColumn("added_to_watchlist", lit("No"))
        .withColumn(
            "completed",
            when(col("completion_pct") >= 90, "Yes").otherwise("No")
        )
        .withColumn("recommendation_source", lit("Live"))
        .withColumn("engagement_level", lit("Live"))
        .withColumn(
            "binge_watch",
            when(col("watch_seconds") >= 7200, "Yes").otherwise("No")
        )
        .select(watch.columns)
    )

    # =====================================================
    # Historical + Live
    # =====================================================

    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    # =====================================================
    # Join Users (includes newly streamed users after load_all_users.py)
    # =====================================================

    all_watch = all_watch.join(
        users.select("user_id", "country"),
        "user_id",
        "left"
    )

    # =====================================================
    # Country Statistics
    # =====================================================

    result = (
        all_watch
        .groupBy("country")
        .agg(
            count("*").alias("views"),

            countDistinct("user_id").alias("unique_users"),

            round(
                avg("watch_minutes"),
                2
            ).alias("avg_watch_minutes"),

            round(
                avg("completion_pct"),
                2
            ).alias("avg_completion")
        )
        .orderBy(col("views").desc())
    )

    output = GOLD_DIR / "country_stats"

    result.write.mode("overwrite").parquet(str(output))

    print(f"Rows : {result.count():,}")
    print(f"Saved : {output}")

    return result