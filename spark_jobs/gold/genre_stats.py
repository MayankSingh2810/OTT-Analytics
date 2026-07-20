from pyspark.sql.functions import (
    count,
    countDistinct,
    avg,
    round,
    desc,
    sum,
    col,
    lit,
    when
)

from config import SILVER_DIR, GOLD_DIR


def build_genre_analytics(spark):

    print("=" * 70)
    print("Building Genre Analytics")
    print("=" * 70)

    # =====================================================
    # Historical
    # =====================================================

    watch = spark.read.parquet(str(SILVER_DIR / "watch_history"))
    content = spark.read.parquet(str(SILVER_DIR / "content"))

    # =====================================================
    # Live Events
    # =====================================================

    live = spark.read.parquet(str(SILVER_DIR / "live_events"))

    live = (
        live
        .drop("genre")
        .join(
            content.select("content_id", "genre", "imdb_rating"),
            "content_id",
            "left"
        )
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
    # Genre Analytics
    # =====================================================

    genre = (
        all_watch
        .join(content, "content_id")
        .groupBy("genre")
        .agg(
            count("*").alias("total_views"),

            countDistinct("user_id").alias("unique_viewers"),

            round(
                avg("watch_minutes"),
                2
            ).alias("avg_watch_minutes"),

            round(
                avg("completion_pct"),
                2
            ).alias("avg_completion"),

            round(
                avg("imdb_rating"),
                2
            ).alias("avg_imdb_rating"),

            round(
                sum("watch_minutes") / 60,
                2
            ).alias("total_watch_hours"),

            round(
                avg(
                    when(col("liked") == "Yes", 1).otherwise(0)
                ),
                2
            ).alias("like_rate"),

            round(
                avg(
                    when(col("completed") == "Yes", 1).otherwise(0)
                ),
                2
            ).alias("completion_rate"),

            round(
                avg(
                    when(col("binge_watch") == "Yes", 1).otherwise(0)
                ),
                2
            ).alias("binge_watch_rate")
        )
        .orderBy(desc("total_views"))
    )

    output = GOLD_DIR / "genre_analytics"

    genre.write.mode("overwrite").parquet(str(output))

    print(f"Rows : {genre.count():,}")
    print(f"Saved : {output}")

    return genre