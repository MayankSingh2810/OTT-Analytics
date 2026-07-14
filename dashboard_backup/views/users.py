import streamlit as st
import plotly.express as px

from components.cards import metric_card

from utils.mysql_loader import (
    load_dashboard_summary,
    load_device_stats,
    load_country_stats,
)


def show():

    summary = load_dashboard_summary()
    devices = load_device_stats()
    countries = load_country_stats()

    st.title("👥 User Analytics")

    st.caption("Platform Activity • Device Intelligence • Geographic Insights")

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    metric_card(
        "Unique Users",
        f"{int(summary.unique_users.iloc[0]):,}",
        "Platform Users",
        "👥",
    )

    metric_card(
        "Avg Watch Time",
        f"{summary.avg_watch_seconds.iloc[0]:.0f}s",
        "Per Event",
        "⏱️",
    )

    metric_card(
        "Countries",
        f"{len(countries)}",
        "Active Regions",
        "🌍",
    )

    metric_card(
        "Devices",
        f"{len(devices)}",
        "Supported",
        "📱",
    )

    st.divider()

    left, right = st.columns(2)

    with left:

        fig = px.bar(
            devices,
            x="device",
            y="total_events",
            color="device",
            template="plotly_dark",
            title="User Activity by Device",
        )

        fig.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font=dict(color="white"),
            coloraxis_showscale=False,
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        fig = px.pie(
            countries,
            names="country",
            values="total_events",
            hole=.45,
            template="plotly_dark",
            title="Users by Country",
        )

        fig.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font=dict(color="white"),
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    fig = px.scatter(
        countries,
        x="avg_watch_seconds",
        y="avg_buffer_ms",
        size="total_events",
        hover_name="country",
        template="plotly_dark",
        title="Watch Time vs Buffer Time",
    )

    fig.update_layout(
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="white"),
    )

    st.plotly_chart(fig, use_container_width=True)