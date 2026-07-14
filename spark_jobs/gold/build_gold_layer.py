"""
==========================================================
Enterprise Gold Layer Builder
==========================================================
"""

from spark_jobs.spark_session import create_spark_session

from spark_jobs.gold.country_stats import build_country_stats
from spark_jobs.gold.device_stats import build_device_stats
from spark_jobs.gold.genre_stats import build_genre_analytics
from spark_jobs.gold.hourly_usage import build_hourly_usage
from spark_jobs.gold.quality_stats import build_quality_stats

from spark_jobs.gold.daily_active_users import build_daily_active_users
from spark_jobs.gold.monthly_active_users import build_monthly_active_users
from spark_jobs.gold.watch_time_summary import build_watch_time_summary

from spark_jobs.gold.subscription_revenue import build_subscription_revenue
from spark_jobs.gold.top_content import build_top_content
from spark_jobs.gold.content_performance import build_content_performance

from spark_jobs.gold.user_retention import build_user_retention
from spark_jobs.gold.churn_features import build_churn_features

from spark_jobs.gold.dashboard_summary import build_dashboard_summary


def build_gold_layer():

    spark = create_spark_session()

    print("\n")
    print("=" * 80)
    print("BUILDING ENTERPRISE GOLD LAYER")
    print("=" * 80)

    # -----------------------------------------------------
    # User Analytics
    # -----------------------------------------------------

    build_daily_active_users(spark)
    build_monthly_active_users(spark)
    build_user_retention(spark)

    # -----------------------------------------------------
    # Content Analytics
    # -----------------------------------------------------

    build_top_content(spark)
    build_content_performance(spark)
    build_genre_analytics(spark)

    # -----------------------------------------------------
    # Platform Analytics
    # -----------------------------------------------------

    build_country_stats(spark)
    build_device_stats(spark)
    build_hourly_usage(spark)
    build_quality_stats(spark)

    # -----------------------------------------------------
    # Revenue
    # -----------------------------------------------------

    build_subscription_revenue(spark)
    build_watch_time_summary(spark)

    # -----------------------------------------------------
    # ML
    # -----------------------------------------------------

    build_churn_features(spark)

    # -----------------------------------------------------
    # Executive
    # -----------------------------------------------------

    build_dashboard_summary(spark)

    spark.stop()

    print("\n")
    print("=" * 80)
    print("GOLD LAYER COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    build_gold_layer()