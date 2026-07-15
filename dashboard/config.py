"""
==========================================================
OTT Stream Intelligence
Dashboard Configuration
==========================================================
"""

# ==========================================================
# STREAMLIT
# ==========================================================

APP_TITLE = "OTT Stream Intelligence"

REFRESH_SECONDS = 10

# ==========================================================
# MYSQL
# ==========================================================

MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASSWORD = "1234"
MYSQL_DATABASE = "ott_analytics"

# ==========================================================
# MYSQL TABLES
# ==========================================================

TABLES = {

    "dashboard": "dashboard_summary",

    "daily_users": "daily_active_users",

    "monthly_users": "monthly_active_users",

    "retention": "user_retention",

    "watch_time": "watch_time_summary",

    "genre": "genre_stats",

    "top_content": "top_content",

    "content": "content_performance",

    "country": "country_stats",

    "device": "device_stats",

    "hourly": "hourly_usage",

    "quality": "quality_stats",

    "revenue": "subscription_revenue",

    "network": "network_stats",

    "popular": "popular_content",

    "event": "event_stats",

    "churn": "churn_features"

}