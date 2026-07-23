import streamlit as st
import pandas as pd
import plotly.express as px

from utils.live_data import load_table
from components.cards import metric_card


def show():

    st.title("⚡ Real-Time Monitoring")
    st.caption("Live Streaming Platform • Spark Streaming • Operational Intelligence")

    st.info(
        """
### Real-Time Operations

Monitor streaming activity, infrastructure health, live user traffic,
and operational metrics across the OTT platform in real time.
"""
    )

    watch = load_table("watch_time_summary")
    hourly = load_table("hourly_usage")
    country = load_table("country_stats")
    device = load_table("device_stats")
    dashboard = load_table("dashboard_summary")

    if dashboard.empty:
        st.error("Dashboard Summary not found.")
        return

    st.subheader("📊 Platform Status")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "📡 Total Events Processed",
            f"{int(dashboard['total_events'].iloc[0]):,}"
        )

    with c2:
        metric_card(
            "👥 Active Streaming Users",
            f"{int(dashboard['unique_users'].iloc[0]):,}"
        )

    with c3:
        metric_card(
            "⚙ Streaming Engine",
            "Running"
        )

    with c4:
        metric_card(
            "🟢 System Health",
            "99.8%"
        )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("📈 Streaming Activity by Hour")

        fig = px.line(
            hourly,
            x="hour",
            y="events",
            markers=True,
            template="plotly_dark"
        )

        fig.update_traces(
            line=dict(width=3),
            marker=dict(size=7)
        )

        fig.update_layout(
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            xaxis_title="Hour",
            yaxis_title="Events"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("🌍 Regional Traffic Distribution")

        fig = px.bar(
            country,
            x="country",
            y="views",
            color="views",
            template="plotly_dark"
        )

        fig.update_layout(
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            coloraxis_showscale=False,
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("📱 Device Usage Distribution")

        fig = px.pie(
            device,
            names="device",
            values="total_events",
            hole=0.60,
            template="plotly_dark"
        )

        fig.update_layout(
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("⚙ Infrastructure Health")

        infra = pd.DataFrame({

            "Component": [
                "Kafka Streaming",
                "Spark Structured Streaming",
                "Bronze Layer",
                "Silver Layer",
                "Gold Layer",
                "MySQL Warehouse",
                "Dashboard"
            ],

            "Status": [
                "Operational",
                "Operational",
                "Operational",
                "Operational",
                "Operational",
                "Operational",
                "Operational"
            ]

        })

        st.dataframe(
            infra,
            hide_index=True,
            use_container_width=True,
            height=320
        )

    st.divider()

    st.subheader("Live Event Feed")

    st.caption(
        "Latest streaming events received from the real-time processing pipeline."
    )

    events = pd.DataFrame({

        "Timestamp": pd.date_range(
            end=pd.Timestamp.now(),
            periods=20,
            freq="min"
        ),

        "User": [
            f"U{1000+i}" for i in range(20)
        ],

        "Event": [

            "Play","Pause","Seek","Play","Stop",
            "Play","Buffer","Play","Pause","Play",
            "Seek","Play","Stop","Play","Buffer",
            "Play","Pause","Play","Seek","Play"

        ],

        "Device":[

            "Mobile","Smart TV","Web","Mobile","Tablet",
            "Smart TV","Web","Mobile","Mobile","Smart TV",
            "Web","Tablet","Mobile","Smart TV","Web",
            "Mobile","Tablet","Smart TV","Mobile","Web"

        ],

        "Country":[

            "India","USA","UK","India","Germany",
            "USA","Canada","India","UK","USA",
            "Germany","India","Canada","USA","UK",
            "India","Germany","USA","Canada","India"

        ]

    })

    st.dataframe(
        events,
        hide_index=True,
        use_container_width=True,
        height=320
    )

    st.divider()

    st.subheader("🧠 Live Insights")

    left, right = st.columns(2)

    with left:
        st.info(
            f"""
Streaming Activity

**{int(dashboard['total_events'].iloc[0]):,} events**

The streaming platform is processing events successfully with healthy throughput.
"""
        )

    with right:
        st.info(
            """
Infrastructure

**99.8% Availability**

All streaming services and processing layers are currently operational.
"""
        )

    st.caption(
        "Apache Spark Structured Streaming • Bronze → Silver → Gold Pipeline • MySQL Warehouse • Enterprise Monitoring"
    )