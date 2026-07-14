import streamlit as st
import plotly.express as px

from components.cards import metric_card

from utils.mysql_loader import (
    load_hourly_usage,
    load_network_stats,
    load_event_stats,
)


def show():

    # ==========================================================
    # LOAD DATA
    # ==========================================================

    hourly = load_hourly_usage()

    network = load_network_stats()

    events = load_event_stats()

    # ==========================================================
    # HEADER
    # ==========================================================

    st.title("🛰️ Real-Time Monitoring")

    st.caption(
        "Streaming Infrastructure • Event Monitoring • Network Performance"
    )

    st.divider()

    # ==========================================================
    # KPI CARDS
    # ==========================================================

    c1, c2, c3 = st.columns(3)

    with c1:

        metric_card(
            "Peak Hour",
            str(hourly["hour"].iloc[hourly["events"].idxmax()]),
            "Highest Traffic",
            "🔥"
        )

    with c2:

        metric_card(
            "Total Events",
            f"{events['events'].sum():,}",
            "Processed",
            "📺"
        )

    with c3:

        metric_card(
            "Networks",
            str(len(network)),
            "Connected",
            "🌐"
        )

    st.divider()

    # ==========================================================
    # Hourly Usage
    # ==========================================================

    fig = px.line(
        hourly,
        x="hour",
        y="events",
        markers=True,
        template="plotly_dark",
        title="Hourly Streaming Activity"
    )

    fig.update_layout(
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ==========================================================
    # Network Usage
    # ==========================================================

    fig = px.bar(
        network,
        x="network_type",
        y="events",
        color="network_type",
        template="plotly_dark",
        title="Streaming by Network"
    )

    fig.update_layout(
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="white"),
        coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ==========================================================
    # Event Distribution
    # ==========================================================

    fig = px.pie(
        events,
        names="event",
        values="events",
        hole=0.5,
        template="plotly_dark",
        title="Event Distribution"
    )

    fig.update_layout(
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

    st.success(
        "✅ Bronze → Silver → Gold → MySQL → Streamlit pipeline is operational."
    )