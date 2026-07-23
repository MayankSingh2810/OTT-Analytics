import streamlit as st

from utils.live_data import load_table
from components.cards import metric_card
from components.charts import bar_chart


def show():

    st.title("👥 User Analytics")
    st.caption("Enterprise Audience Behavior Dashboard")

    st.info(
        """
### Audience Intelligence

Analyze subscriber activity, engagement patterns,
retention trends and user demographics to understand
customer behaviour across the OTT platform.
"""
    )

    retention = load_table("user_retention")
    daily = load_table("daily_active_users")
    monthly = load_table("monthly_active_users")
    dashboard = load_table("dashboard_summary")

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
                "👥 Registered Subscribers",
                f"{int(dashboard['unique_users'].iloc[0]):,}"
            )
        else:
            metric_card("👥 Registered Subscribers", f"{len(retention):,}")

    with c2:

        if "total_sessions" in retention.columns:
            metric_card(
                "🎬 Average Sessions",
                f"{retention['total_sessions'].mean():.1f}"
            )
        else:
            metric_card("🎬 Average Sessions", "N/A")

    with c3:

        if "avg_watch_minutes" in retention.columns:
            metric_card(
                "⏱ Average Watch Time",
                f"{retention['avg_watch_minutes'].mean():.1f} min"
            )
        else:
            metric_card("⏱ Average Watch Time", "N/A")

    with c4:

        if "days_inactive" in retention.columns:
            metric_card(
                "😴 Average Inactive Days",
                f"{retention['days_inactive'].mean():.1f}"
            )
        else:
            metric_card("😴 Average Inactive Days", "N/A")

    st.divider()

    if {"country"}.issubset(retention.columns):

        st.subheader("🌍 Subscriber Distribution")

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
            "Subscriber Distribution"
        )

    st.divider()

    if {"age_group"}.issubset(retention.columns):

        st.subheader("📊 Audience Age Distribution")

        age = (
            retention.groupby("age_group")
            .size()
            .reset_index(name="users")
        )

        age["age_group"] = age["age_group"].astype(str)

        age = age.sort_values("age_group")

        bar_chart(
            age,
            "age_group",
            "users",
            "Audience Age Distribution"
        )

    st.divider()

    if {"membership_years"}.issubset(retention.columns):

        st.subheader("📅 Membership Tenure")

        membership = (
            retention.groupby("membership_years")
            .size()
            .reset_index(name="users")
            .sort_values("membership_years")
        )

        bar_chart(
            membership,
            "membership_years",
            "users",
            "Membership Tenure"
        )

    st.divider()

    if "user_status" in retention.columns:

        active = (
            retention["user_status"]
            .eq("Active")
            .mean()
            * 100
        )

        inactive = 100 - active

        left, right = st.columns(2)

        with left:
            metric_card(
                "🟢 Active Subscribers",
                f"{active:.1f}%"
            )

        with right:
            metric_card(
                "🔴 Inactive Subscribers",
                f"{inactive:.1f}%"
            )

    st.divider()

    if not daily.empty:

        st.subheader("Daily Active Users")

        with st.container(border=True):
            st.dataframe(
                daily,
                use_container_width=True,
                height=320
            )

    if not monthly.empty:

        st.subheader("Monthly Active Users")

        with st.container(border=True):
            st.dataframe(
                monthly,
                use_container_width=True,
                height=320
            )

    st.divider()

    st.subheader("🧠 Audience Insights")

    c1, c2 = st.columns(2)

    with c1:

        if "avg_watch_minutes" in retention.columns:
            st.info(
                f"""
Average Watch Time

**{retention['avg_watch_minutes'].mean():.1f} minutes**

Average watch time indicates sustained user engagement across the platform.
"""
            )

    with c2:

        if "days_inactive" in retention.columns:
            st.info(
                f"""
Average Inactivity

**{retention['days_inactive'].mean():.1f} days**

Subscribers with prolonged inactivity represent the highest retention risk.
"""
            )