"""
============================================================
Gold Layer
Top Content Analytics
============================================================
"""

from pyspark.sql.functions import (
    count,
    avg,
    round,
    desc,
    col,
    when,
    lit
)

from config import SILVER_DIR, GOLD_DIR


def build_top_content(spark):

    print("=" * 70)
    print("Building Top Content")
    print("=" * 70)

    watch = spark.read.parquet(
        str(SILVER_DIR / "watch_history")
    )

    live = spark.read.parquet(
        str(SILVER_DIR / "live_events")
    )

    content = spark.read.parquet(
        str(SILVER_DIR / "content")
    )

    # Convert live events into watch-history format
    live = (
        live
        .withColumn("watch_minutes", round(col("watch_seconds") / 60, 2))
        .withColumn("completion_pct", col("completion_pct"))
        .withColumn("liked", when(col("event_type") == "LIKE", "Yes").otherwise("No"))
        .withColumn("completed", when(col("completion_pct") >= 90, "Yes").otherwise("No"))
        .select(watch.columns)
    )

    # Historical + Live
    all_watch = watch.unionByName(
        live,
        allowMissingColumns=True
    )

    top = (
        all_watch
        .groupBy("content_id")
        .agg(
            count("*").alias("views"),
            round(avg("completion_pct"), 2).alias("avg_completion")
        )
        .join(content, "content_id")
        .orderBy(desc("views"))
    )

    output = GOLD_DIR / "top_content"

    top.write.mode("overwrite").parquet(str(output))

    print(f"Rows : {top.count():,}")
    print(f"Saved : {output}")

    return top