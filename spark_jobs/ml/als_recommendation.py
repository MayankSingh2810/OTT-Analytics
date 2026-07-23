from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col, explode, row_number, desc, lit, least
from pyspark.sql.window import Window
from pyspark.ml.feature import StringIndexer
from pyspark.ml.recommendation import ALS

# ==========================================================
# Spark Session
# ==========================================================

spark = (
    SparkSession.builder
    .appName("OTT Recommendation Engine")
    .getOrCreate()
)

# ==========================================================
# Load Real Interaction Data
# ==========================================================

interactions = spark.read.parquet(
    "data_lake/silver/watch_history"
)

content = spark.read.parquet(
    "data_lake/silver/content"
)

print("Interactions:", interactions.count())

# ==========================================================
# Encode IDs
# ==========================================================

user_indexer = StringIndexer(
    inputCol="user_id",
    outputCol="userIndex"
)

item_indexer = StringIndexer(
    inputCol="content_id",
    outputCol="itemIndex"
)

interactions = user_indexer.fit(interactions).transform(interactions)
interactions = item_indexer.fit(interactions).transform(interactions)

# ==========================================================
# Keep User ID Mapping (for saving results later)
# ==========================================================

user_mapping = (
    interactions
    .select(
        "userIndex",
        "user_id"
    )
    .dropDuplicates(["userIndex"])
)

# ==========================================================
# Keep Item ID Mapping (for joining movie metadata later)
# ==========================================================

item_index_mapping = (
    interactions
    .select("itemIndex", "content_id")
    .dropDuplicates(["itemIndex"])
)

item_mapping = (
    item_index_mapping
    .join(
        content.select("content_id", "title", "genre"),
        on="content_id",
        how="left"
    )
)

# ==========================================================
# Real Rating (derived from actual watch behavior)
# ==========================================================

interactions = interactions.withColumn(
    "rating",
    (
        col("completion_pct") * 0.5
        +
        (least(col("watch_minutes"), lit(180)) / 180.0) * 20
    )
)

interactions = interactions.withColumn(
    "rating",
    when(col("liked") == "Yes", col("rating") + 10)
    .otherwise(col("rating"))
)

interactions = interactions.withColumn(
    "rating",
    when(col("completed") == "Yes", col("rating") + 10)
    .otherwise(col("rating"))
)

interactions = interactions.withColumn(
    "rating",
    when(col("binge_watch") == "Yes", col("rating") + 10)
    .otherwise(col("rating"))
)

interactions = interactions.withColumn(
    "rating",
    when(col("rating") > 100, lit(100))
    .otherwise(col("rating"))
)

# ==========================================================
# Keep Watched Content (to filter out later)
# ==========================================================

already_watched = interactions.select(
    "userIndex",
    "itemIndex"
)

# ==========================================================
# Train ALS
# ==========================================================

als = ALS(
    userCol="userIndex",
    itemCol="itemIndex",
    ratingCol="rating",
    rank=20,
    maxIter=10,
    regParam=0.1,
    coldStartStrategy="drop",
    nonnegative=True
)

model = als.fit(interactions)

# ==========================================================
# Recommend Top 100 (before filtering)
# ==========================================================

recommendations = model.recommendForAllUsers(100)

# ==========================================================
# Explode Recommendations
# ==========================================================

recommendations = recommendations.withColumn(
    "recommendation",
    explode("recommendations")
)

recommendations = recommendations.select(
    "userIndex",
    recommendations.recommendation.itemIndex.alias("itemIndex"),
    recommendations.recommendation.rating.alias("PredictedRating")
)

# ==========================================================
# Remove Already Watched Content
# ==========================================================

recommendations = (
    recommendations.join(
        already_watched,
        on=["userIndex", "itemIndex"],
        how="left_anti"
    )
)

# ==========================================================
# Rank Per User, Keep Best 10
# ==========================================================

window = Window.partitionBy("userIndex").orderBy(
    desc("PredictedRating")
)

recommendations = (
    recommendations
    .withColumn(
        "recommendation_rank",
        row_number().over(window)
    )
    .filter(col("recommendation_rank") <= 10)
)

# ==========================================================
# Join Movie Metadata
# ==========================================================

recommendations = (
    recommendations
    .join(
        item_mapping,
        on="itemIndex",
        how="left"
    )
)

# ==========================================================
# Join User IDs
# ==========================================================

recommendations = (
    recommendations.join(
        user_mapping,
        on="userIndex",
        how="left"
    )
)

# ==========================================================
# Keep Only Useful Columns (in rank order)
# ==========================================================

recommendations = recommendations.select(
    "user_id",
    "content_id",
    "title",
    "genre",
    "PredictedRating",
    "recommendation_rank"
)

# ==========================================================
# Runtime Verification
# ==========================================================

print()
print("Users :", recommendations.select("user_id").distinct().count())
print("Recommendations :", recommendations.count())
recommendations.show(20, truncate=False)

# ==========================================================
# Save Recommendations
# ==========================================================

recommendations.write.mode("overwrite").parquet(
    "ml_models/als/recommendations"
)

model.write().overwrite().save(
    "ml_models/als/model"
)

print("=" * 70)
print("ALS Recommendation Engine Completed Successfully")
print("=" * 70)

spark.stop()