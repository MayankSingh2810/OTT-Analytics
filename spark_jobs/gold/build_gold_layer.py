"""
==========================================================
Enterprise Gold Layer Builder
Historical + Live Events + Live Users
==========================================================
"""

from spark_jobs.spark_session import create_spark_session

# -----------------------------------------------------
# User Gold Tables
# -----------------------------------------------------

from spark_jobs.gold.load_all_users import build_all_users
from spark_jobs.gold.daily_active_users import build_daily_active_users
from spark_jobs.gold.monthly_active_users import build_monthly_active_users
from spark_jobs.gold.user_retention import build_user_retention

# -----------------------------------------------------
# Content Gold Tables
# -----------------------------------------------------

from spark_jobs.gold.top_content import build_top_content
from spark_jobs.gold.content_performance import build_content_performance
from spark_jobs.gold.genre_stats import build_genre_analytics

# -----------------------------------------------------
# Platform Gold Tables
# -----------------------------------------------------

from spark_jobs.gold.country_stats import build_country_stats
from spark_jobs.gold.device_stats import build_device_stats
from spark_jobs.gold.hourly_usage import build_hourly_usage
from spark_jobs.gold.quality_stats import build_quality_stats

# -----------------------------------------------------
# Revenue
# -----------------------------------------------------

from spark_jobs.gold.subscription_revenue import build_subscription_revenue
from spark_jobs.gold.watch_time_summary import build_watch_time_summary

# -----------------------------------------------------
# Machine Learning
# -----------------------------------------------------

from spark_jobs.gold.churn_features import build_churn_features

# -----------------------------------------------------
# Executive Dashboard
# -----------------------------------------------------

from spark_jobs.gold.dashboard_summary import build_dashboard_summary


def build_gold_layer():

    spark = create_spark_session()

    print("\n")
    print("=" * 80)
    print("BUILDING ENTERPRISE GOLD LAYER")
    print("=" * 80)

    # =====================================================
    # STEP 1
    # Merge Historical Users + Live Users
    # =====================================================

    build_all_users(spark)

    # =====================================================
    # STEP 2
    # User Analytics
    # =====================================================

    build_daily_active_users(spark)
    build_monthly_active_users(spark)
    build_user_retention(spark)

    # =====================================================
    # STEP 3
    # Content Analytics
    # =====================================================

    build_top_content(spark)
    build_content_performance(spark)
    build_genre_analytics(spark)

    # =====================================================
    # STEP 4
    # Platform Analytics
    # =====================================================

    build_country_stats(spark)
    build_device_stats(spark)
    build_hourly_usage(spark)
    build_quality_stats(spark)

    # =====================================================
    # STEP 5
    # Revenue
    # =====================================================

    build_subscription_revenue(spark)
    build_watch_time_summary(spark)

    # =====================================================
    # STEP 6
    # Machine Learning
    # =====================================================

    build_churn_features(spark)

    # =====================================================
    # STEP 7
    # Executive Dashboard
    # =====================================================

    build_dashboard_summary(spark)

    spark.stop()

    print("\n")
    print("=" * 80)
    print("ENTERPRISE GOLD LAYER COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    build_gold_layer()