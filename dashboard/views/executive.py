import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.live_data import load_table

from components.insights import (
    executive_insights,
    pipeline_status,
)


def show():

    dashboard = load_table("dashboard_summary")

    st.title("🎬 OTT Stream Intelligence Platform")
    st.caption("Enterprise Big Data Analytics Dashboard")

    st.info(
        """
### Enterprise Overview

This dashboard provides real-time visibility into platform usage,
content performance,
subscriber behaviour,
machine learning predictions,
recommendation quality,
and business intelligence across the OTT ecosystem.
"""
    )

    if dashboard.empty:
        st.error("Dashboard Summary not found.")
        return

    row = dashboard.iloc[0]

    st.divider()

    # ======================================================
    # KPI CARDS
    # ======================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "🎥 Total Watch Hours",
            f"{row['watch_hours']:,.0f}"
        )

    with c2:
        st.metric(
            "👥 Registered Subscribers",
            f"{int(row['registered_users']):,}"
        )

    with c3:
        st.metric(
            "📺 Content Catalog",
            f"{int(row['content_library']):,}"
        )

    with c4:
        st.metric(
            "⭐ Average Completion Rate",
            f"{row['avg_completion']:.2f}%"
        )

    st.divider()

    # ======================================================
    # OVERVIEW + PIPELINE
    # ======================================================

    left, right = st.columns([2.5, 1])

    with left:

        st.subheader("📊 Platform Overview")

        overview_df = pd.DataFrame(
            {
                "Metric": [
                    "Total Events",
                    "Unique Users",
                    "Unique Content",
                    "Average Watch Time",
                    "Completion Rate",
                    "Like Rate",
                    "Binge Watch Rate",
                ],
                "Value": [
                    f"{int(row['total_events']):,}",
                    f"{int(row['unique_users']):,}",
                    f"{int(row['unique_content']):,}",
                    f"{row['avg_watch_minutes']:.2f} min",
                    f"{row['completion_rate']*100:.2f}%",
                    f"{row['like_rate']*100:.2f}%",
                    f"{row['binge_watch_rate']*100:.2f}%"
                ]
            }
        )

        st.dataframe(
            overview_df,
            hide_index=True,
            use_container_width=True,
            height=280
        )

    with right:

        pipeline_status()

    st.divider()

    # ======================================================
    # AI INSIGHTS
    # ======================================================

    executive_insights(row)

    st.divider()

    # ======================================================
    # PLATFORM PERFORMANCE OVERVIEW
    # ======================================================

    st.subheader("📈 Platform Performance Overview")

    chart1, chart2 = st.columns(2)

    with chart1:

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=row["completion_rate"] * 100,
                title={"text": "Completion Rate"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#3BA8FF"},
                    "steps": [
                        {"range": [0, 40], "color": "#3A3A3A"},
                        {"range": [40, 70], "color": "#6A6A6A"},
                        {"range": [70, 100], "color": "#909090"},
                    ],
                },
            )
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0B1220",
            height=350,
        )

        st.plotly_chart(fig, use_container_width=True)

    with chart2:

        health = {
            "Metric": [
                "Like Rate",
                "Completion",
                "Binge Watch"
            ],
            "Value": [
                row["like_rate"] * 100,
                row["completion_rate"] * 100,
                row["binge_watch_rate"] * 100,
            ]
        }

        fig = px.bar(
            health,
            x="Metric",
            y="Value",
            color="Value",
            template="plotly_dark",
        )

        fig.update_layout(
            paper_bgcolor="#0B1220",
            plot_bgcolor="#0B1220",
            coloraxis_showscale=False,
            height=350,
        )

        st.plotly_chart(fig, use_container_width=True)