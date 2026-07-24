import streamlit as st
import pandas as pd

from utils.live_data import load_table
from components.cards import metric_card
from components.charts import pie_chart, bar_chart


def show():

    st.title("Revenue Analytics")
    st.caption("Enterprise Revenue Performance Dashboard")

    st.info(
        """
### Revenue Overview

Track subscription revenue, subscriber growth, renewal performance,
and overall business health across the OTT platform.
"""
    )

    revenue = load_table("subscription_revenue")

    if revenue.empty:
        st.warning("Subscription Revenue table not found.")
        return

    row = revenue.iloc[0]

    numeric = [
        "monthly_revenue",
        "total_subscribers",
        "active_subscribers",
        "average_plan_price",
        "auto_renew_users"
    ]

    for col in numeric:
        if col in revenue.columns:
            revenue[col] = revenue[col].astype(float)

    row = revenue.iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        metric_card(
            "Monthly Revenue",
            f"${row['monthly_revenue']:,.0f}"
        )

    with c2:

        metric_card(
            "Subscribers",
            f"{int(row['total_subscribers']):,}"
        )

    with c3:

        metric_card(
            "Active Subscribers",
            f"{int(row['active_subscribers']):,}"
        )

    with c4:

        metric_card(
            "Avg Plan Price",
            f"${row['average_plan_price']:.2f}"
        )

    st.divider()

    st.subheader("Business Overview")

    summary = pd.DataFrame(
        {
            "Metric": [
                "Monthly Revenue",
                "Subscribers",
                "Active Subscribers",
                "Average Plan Price",
                "Auto Renew Users",
            ],
            "Value": [
                f"${row['monthly_revenue']:,.0f}",
                f"{int(row['total_subscribers']):,}",
                f"{int(row['active_subscribers']):,}",
                f"${row['average_plan_price']:.2f}",
                f"{int(row['auto_renew_users']):,}",
            ],
        }
    )

    st.dataframe(
        summary,
        hide_index=True,
        use_container_width=True,
        height=260,
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        renew = row["auto_renew_users"]
        manual = row["total_subscribers"] - renew

        pie_chart(

            {
                "Type": [
                    "Auto Renew",
                    "Manual"
                ],

                "Users": [
                    renew,
                    manual
                ]

            },

            names="Type",

            values="Users",

            title="Subscription Renewal Distribution"

        )

    with right:

        bar_chart(

            {
                "Metric": [
                    "Revenue",
                    "Subscribers",
                    "Active",
                    "Auto Renew"
                ],

                "Value": [
                    row["monthly_revenue"],
                    row["total_subscribers"],
                    row["active_subscribers"],
                    row["auto_renew_users"]
                ]

            },

            x="Metric",

            y="Value",

            title="Revenue Performance Metrics"

        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Auto-Renew Rate",
            f"{row['auto_renew_users']/row['total_subscribers']*100:.1f}%"
        )

    with col2:

        st.metric(
            "Active Subscriber Rate",
            f"{row['active_subscribers']/row['total_subscribers']*100:.1f}%"
        )

    st.divider()

    st.subheader("Business Health")

    left, right = st.columns(2)

    with left:
        st.success(
            f"""
### Revenue Stability

Average Plan Price

**${row['average_plan_price']:.2f}**

Pricing remains stable across the subscriber base.
"""
        )

    with right:
        st.success(
            f"""
### Subscriber Health

Active Subscribers

**{int(row['active_subscribers']):,}**

The majority of subscribers are currently active.
"""
        )

    st.divider()

    st.subheader("Revenue Insights")

    c1, c2 = st.columns(2)

    with c1:

        st.info(
            f"""
Revenue Performance

**${row['monthly_revenue']:,.0f}**

Recurring subscription revenue remains the primary contributor to platform earnings.
"""
        )

    with c2:

        renewal = (
            row["auto_renew_users"]
            /
            row["total_subscribers"]
            * 100
        )

        st.info(
            f"""
Customer Retention

**{renewal:.1f}%**

A strong renewal rate reflects healthy customer loyalty and recurring revenue stability.
"""
        )