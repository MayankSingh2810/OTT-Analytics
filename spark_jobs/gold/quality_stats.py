"""
==========================================================
Gold Layer
Quality Statistics
(Historical + Live Events)
==========================================================
"""

from pyspark.sql.functions import (
    count,
    avg,
    round,
    desc,
    col,
    lit,
    when
)

from config import SILVER_DIR, GOLD_DIR


def build_quality_stats(spark):

    print("=" * 70)
    print("Building Quality Statistics")
    print("=" * 70)

    # =====================================================
    # Historical
    # =====================================================

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    # =====================================================
    # Live Events
    # =====================================================

    live = spark.read.parquet(
        str(SILVER_DIR / "live_events")
    )

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
            "buffer_ms",
            col("buffer_time_ms")
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

    # =====================================================
    # Historical + Live
    # =====================================================

    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    # =====================================================
    # Quality Statistics
    # =====================================================

    quality = (

        all_watch

        .groupBy("quality")

        .agg(

            count("*").alias("events"),

            round(
                avg("watch_minutes"),
                2
            ).alias("avg_watch_minutes"),

            round(
                avg("completion_pct"),
                2
            ).alias("avg_completion"),

            round(
                avg("buffer_ms"),
                2
            ).alias("avg_buffer_ms")

        )

        .orderBy(
            desc("events")
        )

    )

    output = GOLD_DIR / "quality_stats"

    quality.write.mode("overwrite").parquet(
        str(output)
    )

    print(f"Rows : {quality.count():,}")
    print(f"Saved : {output}")

    return quality