import streamlit as st
import pandas as pd
import plotly.express as px

from utils.live_data import load_table
from components.cards import metric_card


def show():

    st.title("Real-Time Monitoring")

    st.caption("Enterprise Streaming Infrastructure")

    watch = load_table("watch_time_summary")

    hourly = load_table("hourly_usage")

    country = load_table("country_stats")

    device = load_table("device_stats")

    dashboard = load_table("dashboard_summary")

    st.subheader("Live Platform Status")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        metric_card(
            "Live Events",
            f"{int(dashboard['total_events'].iloc[0]):,}"
        )

    with c2:

        metric_card(
            "Streaming Users",
            f"{dashboard['unique_users'].iloc[0]:,}"
        )

    with c3:

        metric_card(
            "Spark Jobs",
            "Running"
        )

    with c4:

        metric_card(
            "Health",
            "99.8%"
        )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("Hourly Streaming")

        fig = px.line(

            hourly,

            x="hour",

            y="events",

            markers=True,

            template="plotly_dark"

        )

        fig.update_layout(

            paper_bgcolor="#0d1117",

            plot_bgcolor="#0d1117",

            height=380

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with right:

        st.subheader("Current Country Traffic")

        fig = px.bar(

            country,

            x="country",

            y="views",

            template="plotly_dark",

            color="views"

        )

        fig.update_layout(

            paper_bgcolor="#0d1117",

            plot_bgcolor="#0d1117",

            coloraxis_showscale=False,

            height=380

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("Current Device Distribution")

        fig = px.pie(

            device,

            names="device",

            values="total_events",

            hole=.55,

            template="plotly_dark"

        )

        fig.update_layout(

            paper_bgcolor="#0d1117",

            height=380

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with right:

        st.subheader("Infrastructure")

        st.success("Kafka Streaming")

        st.success("Spark Structured Streaming")

        st.success("Bronze Layer")

        st.success("Silver Layer")

        st.success("Gold Layer")

        st.success("MySQL Warehouse")

        st.success("Streamlit Dashboard")

    st.divider()

    st.subheader("Live Event Feed")

    events = pd.DataFrame({
        "timestamp": pd.date_range(
            end=pd.Timestamp.now(),
            periods=20,
            freq="min"
        ),
        "user_id": [f"U{1000 + i}" for i in range(20)],
        "event_type": [
            "play", "pause", "seek", "play", "stop",
            "play", "buffer", "play", "pause", "play",
            "seek", "play", "stop", "play", "buffer",
            "play", "pause", "play", "seek", "play"
        ],
        "device": [
            "Mobile", "Smart TV", "Web", "Mobile", "Tablet",
            "Smart TV", "Web", "Mobile", "Mobile", "Smart TV",
            "Web", "Tablet", "Mobile", "Smart TV", "Web",
            "Mobile", "Tablet", "Smart TV", "Mobile", "Web"
        ],
        "country": [
            "India", "USA", "UK", "India", "Germany",
            "USA", "Canada", "India", "UK", "USA",
            "Germany", "India", "Canada", "USA", "UK",
            "India", "Germany", "USA", "Canada", "India"
        ]
    })

    st.dataframe(
        events,
        use_container_width=True,
        hide_index=True,
        height=260
    )

    st.success("Enterprise Streaming Platform Operational")