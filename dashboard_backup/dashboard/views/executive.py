import streamlit as st

from components.cards import metric_card

from components.charts import (
    device_chart,
    country_chart,
    genre_chart,
    subscription_chart,
    top_content_chart,
    completion_gauge,
)

from utils.mysql_loader import (
    load_dashboard_summary,
    load_device_stats,
    load_country_stats,
    load_genre_stats,
    load_subscription_stats,
    load_popular_content,
)


def show():

    # ==========================================================
    # LOAD MYSQL DATA
    # ==========================================================

    summary = load_dashboard_summary()
    devices = load_device_stats()
    countries = load_country_stats()
    genres = load_genre_stats()
    subscriptions = load_subscription_stats()
    content = load_popular_content()

    # ==========================================================
    # PAGE HEADER
    # ==========================================================

    st.title("🎬 OTT Stream Intelligence")

    st.caption(
        "Enterprise Big Data Analytics Platform"
    )

    st.divider()

    # ==========================================================
    # KPI CARDS
    # ==========================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        metric_card(
            "Streaming Events",
            f"{int(summary.total_events.iloc[0]):,}",
            "Processed",
            "📺"
        )

    with c2:

        metric_card(
            "Users",
            f"{int(summary.unique_users.iloc[0]):,}",
            "Registered",
            "👥"
        )

    with c3:

        metric_card(
            "Content",
            f"{int(summary.unique_content.iloc[0]):,}",
            "Titles",
            "🎬"
        )

    with c4:

        metric_card(
            "Completion",
            f"{summary.avg_completion.iloc[0]:.2f} %",
            "Average",
            "⭐"
        )

    st.divider()

    # ==========================================================
    # ROW 1
    # ==========================================================

    left, right = st.columns(2)

    with left:

        st.plotly_chart(
            device_chart(devices),
            use_container_width=True
        )

    with right:

        st.plotly_chart(
            subscription_chart(subscriptions),
            use_container_width=True
        )

    st.divider()

    # ==========================================================
    # ROW 2
    # ==========================================================

    left, right = st.columns([2,1])

    with left:

        st.plotly_chart(
            country_chart(countries),
            use_container_width=True
        )

    with right:

        st.plotly_chart(
            completion_gauge(summary),
            use_container_width=True
        )

    st.divider()

    # ==========================================================
    # ROW 3
    # ==========================================================

    st.plotly_chart(
        genre_chart(genres),
        use_container_width=True
    )

    st.divider()

    # ==========================================================
    # ROW 4
    # ==========================================================

    st.plotly_chart(
        top_content_chart(content),
        use_container_width=True
    )

    st.divider()

    # ==========================================================
    # FOOTER
    # ==========================================================

    st.success(
        """
✅ Enterprise Big Data Pipeline Operational

Bronze → Silver → Gold → MySQL → Streamlit

Apache Spark • PySpark • MySQL • Plotly • Streamlit
"""
    )