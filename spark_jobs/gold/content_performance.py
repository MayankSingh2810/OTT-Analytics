"""
==========================================================
Gold Layer
Content Performance
(Historical + Live Events)
==========================================================
"""

from pyspark.sql.functions import (
    count,
    avg,
    round,
    desc,
    when,
    col,
    lit
)

from config import SILVER_DIR, GOLD_DIR


def build_content_performance(spark):

    print("=" * 70)
    print("Building Content Performance")
    print("=" * 70)

    # ----------------------------------------------------
    # Historical Watch History
    # ----------------------------------------------------

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    # ----------------------------------------------------
    # Live Events
    # ----------------------------------------------------

    live = spark.read.parquet(
        str(SILVER_DIR / "live_events")
    )

    content = spark.read.parquet(
        str(SILVER_DIR / "content")
    )

    # ----------------------------------------------------
    # Convert Live Events
    # ----------------------------------------------------

    live = (

        live

        .withColumn("watch_id", col("event_id"))
        .withColumn("watch_start", col("timestamp"))
        .withColumn("watch_end", col("timestamp"))

        .withColumn(
            "watch_minutes",
            round(col("watch_seconds") / 60, 2)
        )

        .withColumn(
            "liked",
            when(col("event_type") == "LIKE", "Yes")
            .otherwise("No")
        )

        .withColumn(
            "completed",
            when(col("completion_pct") >= 90, "Yes")
            .otherwise("No")
        )

        .withColumn("added_to_watchlist", lit("No"))
        .withColumn("recommendation_source", lit("Live"))
        .withColumn("engagement_level", lit("Live"))
        .withColumn(
            "binge_watch",
            when(col("watch_seconds") >= 7200, "Yes")
            .otherwise("No")
        )

        .select(watch.columns)

    )

    # ----------------------------------------------------
    # Historical + Live
    # ----------------------------------------------------

    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    # ----------------------------------------------------
    # Content Performance
    # ----------------------------------------------------

    performance = (

        all_watch

        .join(content, "content_id")

        .groupBy(
            "content_id",
            "title",
            "genre"
        )

        .agg(

            count("*").alias("views"),

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
            ).alias("avg_rating"),

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

        .orderBy(desc("views"))

    )

    output = GOLD_DIR / "content_performance"

    performance.write.mode("overwrite").parquet(
        str(output)
    )

    print(f"Rows : {performance.count():,}")
    print(f"Saved : {output}")

    return performance