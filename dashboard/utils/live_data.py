import pandas as pd
from sqlalchemy import create_engine

MYSQL_USER = "root"
MYSQL_PASSWORD = "1234"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DATABASE = "ott_analytics"

engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)

TABLES = {
    # short aliases
    "dashboard": "dashboard_summary",
    "daily_users": "daily_active_users",
    "monthly_users": "monthly_active_users",
    "retention": "user_retention",
    "watch_time": "watch_time_summary",
    "genre": "genre_analytics",
    "genre_analytics": "genre_analytics",
    "top_content": "top_content",
    "content": "content_performance",
    "country": "country_stats",
    "device": "device_stats",
    "hourly": "hourly_usage",
    "quality": "quality_stats",
    "subscription_revenue": "subscription_revenue",
    "revenue": "subscription_revenue",
    "network": "network_stats",
    "popular": "popular_content",
    "events": "event_stats",
    "churn": "churn_features",

    # full table names (so pages calling load_table("dashboard_summary")
    # etc. also resolve correctly, without having to rewrite every page)
    "dashboard_summary": "dashboard_summary",
    "daily_active_users": "daily_active_users",
    "monthly_active_users": "monthly_active_users",
    "user_retention": "user_retention",
    "watch_time_summary": "watch_time_summary",
    "content_performance": "content_performance",
    "country_stats": "country_stats",
    "device_stats": "device_stats",
    "hourly_usage": "hourly_usage",
    "quality_stats": "quality_stats",
    "network_stats": "network_stats",
    "popular_content": "popular_content",
    "event_stats": "event_stats",
    "churn_features": "churn_features",
    
}


def load_table(name):

    if name not in TABLES:
        print("Unknown table:", name)
        return pd.DataFrame()

    query = f"SELECT * FROM {TABLES[name]}"
    print(query)

    df = pd.read_sql(query, engine)

    print("Loaded:", TABLES[name])
    print(df.shape)
    print(df.head())
    print(df.columns.tolist())

    return df