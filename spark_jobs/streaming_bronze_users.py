from pyspark.sql import SparkSession
from pyspark.sql.types import *

spark = (
    SparkSession.builder
    .appName("OTT Bronze User Streaming")
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

schema = StructType([
    StructField("user_id", StringType()),
    StructField("first_name", StringType()),
    StructField("last_name", StringType()),
    StructField("email", StringType()),
    StructField("gender", StringType()),
    StructField("age", IntegerType()),
    StructField("country", StringType()),
    StructField("city", StringType()),
    StructField("preferred_language", StringType()),
    StructField("preferred_genre", StringType()),
    StructField("device_type", StringType()),
    StructField("profile_type", StringType()),
    StructField("signup_date", StringType()),
    StructField("account_status", StringType()),
    StructField("subscription_plan", StringType())
])

stream = (
    spark.readStream
    .schema(schema)
    .option("maxFilesPerTrigger", 2)
    .json("streaming/new_users")
)

query = (
    stream.writeStream
    .format("parquet")
    .outputMode("append")
    .option("path", "data_lake/bronze/live_users")
    .option("checkpointLocation", "data_lake/checkpoints/bronze_users")
    .trigger(processingTime="5 seconds")
    .start()
)

print("=" * 70)
print("LIVE USER BRONZE STREAM STARTED")
print("=" * 70)

query.awaitTermination()