import streamlit as st
import plotly.express as px

from components.cards import metric_card

from utils.mysql_loader import (
    load_subscription_stats,
    load_dashboard_summary,
)


def show():

    # ==========================================================
    # LOAD DATA
    # ==========================================================

    summary = load_dashboard_summary()
    subscriptions = load_subscription_stats()

    st.title("💰 Revenue Analytics")

    st.caption("Subscription Intelligence • Plan Performance • Revenue Insights")

    st.divider()

    total_events = int(subscriptions["events"].sum())
    plans = len(subscriptions)
    avg_completion = summary["avg_completion"].iloc[0]
    avg_watch = summary["avg_watch_seconds"].iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Subscription Events",
            f"{total_events:,}",
            "All Plans",
            "💳",
        )

    with c2:
        metric_card(
            "Plans",
            f"{plans}",
            "Available",
            "📦",
        )

    with c3:
        metric_card(
            "Avg Completion",
            f"{avg_completion:.2f}%",
            "Platform",
            "📈",
        )

    with c4:
        metric_card(
            "Avg Watch Time",
            f"{avg_watch:.0f}s",
            "Per Event",
            "⏱️",
        )

    st.divider()

    left, right = st.columns(2)

    with left:

        fig = px.bar(
            subscriptions,
            x="subscription_plan",
            y="events",
            color="subscription_plan",
            template="plotly_dark",
            title="Subscription Plan Popularity",
        )

        fig.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font=dict(color="white"),
            coloraxis_showscale=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with right:

        fig = px.pie(
            subscriptions,
            names="subscription_plan",
            values="events",
            hole=.50,
            template="plotly_dark",
            title="Subscription Share",
        )

        fig.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font=dict(color="white"),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.divider()

    fig = px.bar(
        subscriptions.sort_values("events", ascending=False),
        x="subscription_plan",
        y="avg_watch_seconds",
        color="avg_watch_seconds",
        text="avg_watch_seconds",
        template="plotly_dark",
        color_continuous_scale="Reds",
        title="Average Watch Time by Subscription Plan",
    )

    fig.update_layout(
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="white"),
        coloraxis_showscale=False,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )