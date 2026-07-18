"""
==========================================================
Gold Layer
Content Performance
Historical + Live
==========================================================
"""

from pyspark.sql.functions import (
    count,
    avg,
    round,
    desc,
    lit,
    col,
    sum
)

from config import SILVER_DIR, GOLD_DIR


def build_content_performance(spark):

    print("=" * 70)
    print("Building Content Performance")
    print("=" * 70)

    # ----------------------------------------------------
    # Historical Data
    # ----------------------------------------------------

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    content = spark.read.parquet(
        str(SILVER_DIR / "content")
    )

    historical = (

        watch

        .join(content, "content_id")

        .groupBy(
            "content_id",
            "title",
            "genre"
        )

        .agg(

            count("*").alias("hist_views"),

            avg("watch_minutes").alias("hist_watch"),

            avg("completion_pct").alias("hist_completion"),

            avg("imdb_rating").alias("hist_rating")

        )

    )

    # ----------------------------------------------------
    # Live Data
    # ----------------------------------------------------

    live = spark.read.parquet(
        str(SILVER_DIR / "live_events")
    )

    live = (

    live

    .drop("genre")

    .join(
        content.select(
            "content_id",
            "title",
            "genre"
        ),
        "content_id",
        "left"
    )

        .withColumn(
            "watch_minutes",
            col("watch_seconds") / 60
        )

    )

    live_metrics = (

        live

        .groupBy(
            "content_id",
            "title",
            "genre"
        )

        .agg(

            count("*").alias("live_views"),

            avg("watch_minutes").alias("live_watch"),

            avg("completion_pct").alias("live_completion"),

            lit(0).alias("live_rating")

        )

    )

    # ----------------------------------------------------
    # Merge Historical + Live
    # ----------------------------------------------------

    performance = (

        historical.alias("h")

        .join(
            live_metrics.alias("l"),
            ["content_id", "title", "genre"],
            "full"
        )

        .na.fill({
            "hist_views": 0,
            "live_views": 0,
            "hist_watch": 0,
            "live_watch": 0,
            "hist_completion": 0,
            "live_completion": 0,
            "hist_rating": 0
        })

        .select(

            col("content_id"),

            col("title"),

            col("genre"),

            (
                col("hist_views").cast("long")
                +
                col("live_views").cast("long")
            ).alias("views"),

            round(
                col("hist_watch") + col("live_watch"),
                2
            ).alias("avg_watch_minutes"),

            round(
                col("hist_completion") + col("live_completion"),
                2
            ).alias("avg_completion"),

            round(
                col("hist_rating"),
                2
            ).alias("avg_rating")

        )

        .na.fill(0)

        .orderBy(
            desc("views")
        )

    )

    output = GOLD_DIR / "content_performance"

    performance.write.mode("overwrite").parquet(str(output))

    print(f"Rows : {performance.count():,}")
    print(f"Saved : {output}")

    return performance