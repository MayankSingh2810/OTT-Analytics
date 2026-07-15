import streamlit as st

from utils.live_data import load_table
from components.cards import metric_card
from components.charts import pie_chart, bar_chart


def show():

    st.title("💰 Revenue Analytics")
    st.caption("Subscription Revenue Intelligence")

    revenue = load_table("revenue")

    if revenue.empty:
        st.warning("Subscription Revenue table not found.")
        return

    row = revenue.iloc[0]

    # ---------------------------------------------
    # Numeric conversion
    # ---------------------------------------------

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

    # ---------------------------------------------
    # KPI Cards
    # ---------------------------------------------

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
            "Active Users",
            f"{int(row['active_subscribers']):,}"
        )

    with c4:

        metric_card(
            "Average Plan",
            f"${row['average_plan_price']:.2f}"
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

            title="Subscription Renewal"

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

            title="Revenue Snapshot"

        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Auto Renew Rate",
            f"{row['auto_renew_users']/row['total_subscribers']*100:.1f}%"
        )

    with col2:

        st.metric(
            "Active Subscriber Rate",
            f"{row['active_subscribers']/row['total_subscribers']*100:.1f}%"
        )

    st.success("✅ Revenue Analytics Loaded Successfully")