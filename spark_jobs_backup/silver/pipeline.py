from spark_jobs.spark_session import create_spark_session

from spark_jobs.silver.users import transform_users
from spark_jobs.silver.watch_history import transform_watch_history
from spark_jobs.silver.sessions import transform_sessions
from spark_jobs.silver.ratings import transform_ratings
from spark_jobs.silver.search_history import transform_search_history
from spark_jobs.silver.subscriptions import transform_subscriptions
from spark_jobs.silver.content import transform_content

spark = create_spark_session()

transform_users(spark)
transform_watch_history(spark)
transform_sessions(spark)
transform_ratings(spark)
transform_search_history(spark)
transform_subscriptions(spark)
transform_content(spark)

spark.stop()

print("=" * 70)
print("Silver Pipeline Completed")
print("=" * 70)