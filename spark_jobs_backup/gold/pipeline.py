from spark_jobs.spark_session import create_spark_session

# ============================================================
# Existing Analytical Gold Tables
# ============================================================

from spark_jobs.gold.daily_active_users import build_daily_active_users
from spark_jobs.gold.monthly_active_users import build_monthly_active_users
from spark_jobs.gold.watch_time_summary import build_watch_time_summary
from spark_jobs.gold.subscription_revenue import build_subscription_revenue
from spark_jobs.gold.top_content import build_top_content
from spark_jobs.gold.genre_analytics import build_genre_analytics
from spark_jobs.gold.device_usage import build_device_usage
from spark_jobs.gold.user_retention import build_user_retention
from spark_jobs.gold.content_performance import build_content_performance
from spark_jobs.gold.churn_features import build_churn_features

# ============================================================
# Enterprise Dashboard Gold Tables
# ============================================================

from spark_jobs.gold.country_stats import build_country_stats
from spark_jobs.gold.device_stats import build_device_stats
from spark_jobs.gold.network_stats import build_network_stats
from spark_jobs.gold.event_stats import build_event_stats
from spark_jobs.gold.quality_stats import build_quality_stats
from spark_jobs.gold.dashboard_summary import build_dashboard_summary
from spark_jobs.gold.hourly_usage import build_hourly_usage


def run_pipeline():

    spark = create_spark_session()

    print("\n" + "=" * 80)
    print("        BUILDING GOLD LAYER")
    print("=" * 80)

    gold_jobs = [

        ("Daily Active Users", build_daily_active_users),
        ("Monthly Active Users", build_monthly_active_users),
        ("Watch Time Summary", build_watch_time_summary),
        ("Subscription Revenue", build_subscription_revenue),
        ("Top Content", build_top_content),
        ("Genre Analytics", build_genre_analytics),
        ("Device Usage", build_device_usage),
        ("User Retention", build_user_retention),
        ("Content Performance", build_content_performance),
        ("Churn Features", build_churn_features),

        ("Country Stats", build_country_stats),
        ("Device Stats", build_device_stats),
        ("Network Stats", build_network_stats),
        ("Event Stats", build_event_stats),
        ("Quality Stats", build_quality_stats),
        ("Dashboard Summary", build_dashboard_summary),
        ("Hourly Usage", build_hourly_usage),
    ]

    for name, job in gold_jobs:

        print(f"\nBuilding {name}...")

        try:
            job(spark)
            print(f"✓ {name} completed")

        except Exception as e:
            print(f"✗ {name} failed")
            print(e)

    spark.stop()

    print("\n" + "=" * 80)
    print("      GOLD LAYER COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    run_pipeline()