import streamlit as st

from utils.live_data import load_table
from components.cards import metric_card
from components.charts import bar_chart


def show():

    st.title("👥 User Analytics")
    st.caption("Customer Retention & Audience Intelligence")

    retention = load_table("retention")

    if retention.empty:
        st.warning("No User Retention data found.")
        return

    st.subheader("Platform User Statistics")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Registered Users",
            f"{len(retention):,}"
        )

    with c2:
        metric_card(
            "Average Sessions",
            f"{retention.total_sessions.mean():.1f}"
        )

    with c3:
        metric_card(
            "Average Watch Time",
            f"{retention.avg_watch_minutes.mean():.1f} min"
        )

    with c4:
        metric_card(
            "Inactive Days",
            f"{retention.days_inactive.mean():.1f}"
        )

    st.divider()

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

    st.subheader("Age Groups")

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

    st.subheader("Membership Years")

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