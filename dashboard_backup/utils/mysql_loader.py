import pandas as pd
import mysql.connector
import streamlit as st


# ==========================================================
# CONFIG
# ==========================================================

HOST = "localhost"
USER = "root"
PASSWORD = "1234"
DATABASE = "ott_analytics"


# ==========================================================
# GENERIC LOADER
# ==========================================================

@st.cache_data(ttl=60)
def load_table(table_name):

    conn = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )

    query = f"SELECT * FROM {table_name}"

    df = pd.read_sql(query, conn)

    conn.close()

    return df


# ==========================================================
# TABLES
# ==========================================================

def load_dashboard_summary():
    return load_table("dashboard_summary")


def load_device_stats():
    return load_table("device_stats")


def load_country_stats():
    return load_table("country_stats")


def load_genre_stats():
    return load_table("genre_stats")


def load_subscription_stats():
    return load_table("subscription_stats")


def load_event_stats():
    return load_table("event_stats")


def load_quality_stats():
    return load_table("quality_stats")


def load_network_stats():
    return load_table("network_stats")


def load_popular_content():
    return load_table("popular_content")


def load_hourly_usage():
    return load_table("hourly_usage")