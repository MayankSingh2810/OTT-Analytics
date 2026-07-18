from pyspark.sql.functions import (
    count,
    countDistinct,
    avg,
    round,
    desc,
    sum,
    col,
    lit
)

from config import SILVER_DIR, GOLD_DIR


def build_genre_analytics(spark):

    print("=" * 70)
    print("Building Genre Analytics")
    print("=" * 70)

    # Historical
    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    content = spark.read.parquet(
        str(SILVER_DIR / "content")
    )

    # Live
    live = spark.read.parquet(
        str(SILVER_DIR / "live_events")
    )

    live = (
        live
        .drop("genre")
        .join(
            content.select("content_id", "genre", "imdb_rating"),
            "content_id",
            "left"
        )
        .withColumn("watch_minutes", col("watch_seconds") / 60)
        .withColumn("watch_id", col("event_id"))
        .withColumn("watch_start", col("timestamp"))
        .withColumn("watch_end", col("timestamp"))
        .withColumn("liked", lit("No"))
        .withColumn("added_to_watchlist", lit("No"))
        .withColumn("recommendation_source", lit("Live"))
        .withColumn(
            "completed",
            (col("completion_pct") >= 90).cast("string")
        )
        .withColumn("engagement_level", lit("Live"))
        .withColumn("binge_watch", lit("No"))
        .select(watch.columns)
    )

    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    genre = (

        all_watch

        .join(
            content,
            "content_id"
        )

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
            ).alias("total_watch_hours")

        )

        .orderBy(
            desc("total_views")
        )

    )

    output = GOLD_DIR / "genre_analytics"

    genre.write.mode("overwrite").parquet(
        str(output)
    )

    print(f"Rows : {genre.count():,}")
    print(f"Saved : {output}")

    return genre