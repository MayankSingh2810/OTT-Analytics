"""
============================================================
OTT Silver Pipeline
============================================================
"""

from spark_jobs.spark_session import create_spark_session

from spark_jobs.silver.users import transform_users
from spark_jobs.silver.content import transform_content
from spark_jobs.silver.subscriptions import transform_subscriptions
from spark_jobs.silver.watch_history import transform_watch_history
from spark_jobs.silver.ratings import transform_ratings
from spark_jobs.silver.search_history import transform_search_history
from spark_jobs.silver.sessions import transform_sessions


def run_pipeline():

    spark = create_spark_session()

    print("=" * 80)
    print("BUILDING SILVER LAYER")
    print("=" * 80)

    transform_users(spark)
    transform_content(spark)
    transform_subscriptions(spark)
    transform_watch_history(spark)
    transform_ratings(spark)
    transform_search_history(spark)
    transform_sessions(spark)

    spark.stop()

    print("=" * 80)
    print("SILVER LAYER COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    run_pipeline()