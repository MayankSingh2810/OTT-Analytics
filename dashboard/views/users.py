import streamlit as st

from utils.live_data import load_table
from components.cards import metric_card
from components.charts import bar_chart


def show():

    st.title("👥 User Analytics")
    st.caption("Customer Retention & Audience Intelligence")

    retention = load_table("retention")
    daily = load_table("daily_users")
    monthly = load_table("monthly_users")
    dashboard = load_table("dashboard")

    if retention.empty:
        st.warning("User Retention table not found.")
        return

    # -----------------------------------------
    # Convert numeric columns
    # -----------------------------------------

    numeric_cols = [
        "total_sessions",
        "avg_watch_minutes",
        "days_inactive",
        "membership_years",
    ]

    for col in numeric_cols:
        if col in retention.columns:
            retention[col] = retention[col].astype(float)

    st.subheader("Platform User Statistics")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        if not dashboard.empty and "unique_users" in dashboard.columns:
            metric_card(
                "Registered Users",
                f"{int(dashboard['unique_users'].iloc[0]):,}"
            )
        else:
            metric_card("Registered Users", f"{len(retention):,}")

    with c2:

        if "total_sessions" in retention.columns:
            metric_card(
                "Average Sessions",
                f"{retention['total_sessions'].mean():.1f}"
            )
        else:
            metric_card("Average Sessions", "N/A")

    with c3:

        if "avg_watch_minutes" in retention.columns:
            metric_card(
                "Average Watch Time",
                f"{retention['avg_watch_minutes'].mean():.1f} min"
            )
        else:
            metric_card("Average Watch Time", "N/A")

    with c4:

        if "days_inactive" in retention.columns:
            metric_card(
                "Inactive Days",
                f"{retention['days_inactive'].mean():.1f}"
            )
        else:
            metric_card("Inactive Days", "N/A")

    st.divider()

    if {"country"}.issubset(retention.columns):

        st.subheader("Users by Country")

        country = (
            retention.groupby("country")
            .size()
            .reset_index(name="users")
            .sort_values("users", ascending=False)
        )

        bar_chart(
            country,
            "country",
            "users",
            "Users by Country"
        )

    st.divider()

    if {"age_group"}.issubset(retention.columns):

        st.subheader("Age Distribution")

        age = (
            retention.groupby("age_group")
            .size()
            .reset_index(name="users")
        )

        bar_chart(
            age,
            "age_group",
            "users",
            "Age Distribution"
        )

    st.divider()

    if {"membership_years"}.issubset(retention.columns):

        st.subheader("Membership Duration")

        membership = (
            retention.groupby("membership_years")
            .size()
            .reset_index(name="users")
        )

        bar_chart(
            membership,
            "membership_years",
            "users",
            "Membership Duration"
        )

    st.divider()

    if "account_status" in retention.columns:

        active = (
            retention["account_status"]
            .eq("Active")
            .mean()
            * 100
        )

        inactive = 100 - active

        col1, col2 = st.columns(2)

        col1.metric(
            "Active Accounts",
            f"{active:.1f}%"
        )

        col2.metric(
            "Inactive Accounts",
            f"{inactive:.1f}%"
        )

    st.divider()

    if not daily.empty:

        st.subheader("Daily Active Users")

        st.dataframe(
            daily,
            use_container_width=True
        )

    if not monthly.empty:

        st.subheader("Monthly Active Users")

        st.dataframe(
            monthly,
            use_container_width=True
        )

    st.success("✅ User Analytics Loaded Successfully")