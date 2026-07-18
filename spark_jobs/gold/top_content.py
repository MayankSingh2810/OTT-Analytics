"""
==========================================================
Gold Layer
Top Content
Enterprise Version
==========================================================
"""

from pyspark.sql.functions import (
    count,
    countDistinct,
    avg,
    round,
    desc,
    sum,
    when,
    col,
    lit,
    lower,
)

from config import SILVER_DIR, GOLD_DIR


def build_top_content(spark):

    print("=" * 70)
    print("Building Top Content")
    print("=" * 70)

    watch = spark.read.parquet(str(SILVER_DIR / "watch_history"))
    live = spark.read.parquet(str(SILVER_DIR / "live_events"))
    content = spark.read.parquet(str(SILVER_DIR / "content"))

    live = (
        live
        .withColumn("watch_id", col("event_id"))
        .withColumn("watch_start", col("timestamp"))
        .withColumn("watch_end", col("timestamp"))
        .withColumn("watch_minutes", round(col("watch_seconds") / 60, 2))
        .withColumn("recommendation_source", lit("Live"))
        .withColumn(
            "liked",
            when(lower(col("event_type")) == "like", "Yes").otherwise("No")
        )
        .withColumn("added_to_watchlist", lit("No"))
        .withColumn(
            "completed",
            when(col("completion_pct") >= 90, "Yes").otherwise("No")
        )
        .withColumn(
            "engagement_level",
            when(col("watch_seconds") >= 3600, "High")
            .when(col("watch_seconds") >= 1200, "Medium")
            .otherwise("Low")
        )
        .withColumn(
            "binge_watch",
            when(col("watch_seconds") >= 7200, "Yes").otherwise("No")
        )
        .select(
            "watch_id",
            "user_id",
            "content_id",
            "watch_start",
            "watch_end",
            "watch_minutes",
            "completion_pct",
            "device",
            "network",
            "recommendation_source",
            "liked",
            "added_to_watchlist",
            "completed",
            "engagement_level",
            "binge_watch",
        )
    )

    # Combine historical watch history with reshaped live events
    # so every downstream aggregation reflects both sources.
    all_watch = watch.unionByName(live, allowMissingColumns=True)

    top = (
        all_watch
        .join(content, "content_id")
        .groupBy("content_id", "title", "genre", "content_type")
        .agg(
            count("*").alias("views"),
            countDistinct("user_id").alias("unique_viewers"),
            round(avg("watch_minutes"), 2).alias("avg_watch_minutes"),
            round(avg("completion_pct"), 2).alias("avg_completion"),
            round(
                avg(when(col("liked") == "Yes", 1).otherwise(0)), 2
            ).alias("like_rate"),
            round(
                avg(when(col("completed") == "Yes", 1).otherwise(0)), 2
            ).alias("completion_rate"),
            round(
                avg(when(col("binge_watch") == "Yes", 1).otherwise(0)), 2
            ).alias("binge_watch_rate"),
            round(avg("imdb_rating"), 2).alias("imdb_rating"),
            round(sum("watch_minutes") / 60, 2).alias("watch_hours"),
        )
        .orderBy(desc("views"))
    )

    output = GOLD_DIR / "top_content"

    top.write.mode("overwrite").parquet(str(output))

    print(f"Rows  : {top.count():,}")
    print(f"Saved : {output}")

    return top