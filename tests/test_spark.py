from spark_jobs.spark_session import create_spark_session

spark = create_spark_session()

print("=" * 70)

print("Spark Version :", spark.version)

print("Spark Session Created Successfully")

print("=" * 70)

spark.stop()