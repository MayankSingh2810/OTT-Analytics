import streamlit as st
import plotly.express as px

from components.cards import metric_card

from utils.mysql_loader import (
    load_quality_stats,
    load_device_stats,
    load_country_stats,
    load_genre_stats,
)


def show():

    quality = load_quality_stats()
    devices = load_device_stats()
    countries = load_country_stats()
    genres = load_genre_stats()

    st.title("🤖 AI & ML Analytics")

    st.caption(
        "Machine Learning Ready Dataset • Behaviour Intelligence • Model Features"
    )

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Quality Levels",
            f"{len(quality)}",
            "Streaming Profiles",
            "🎥",
        )

    with c2:
        metric_card(
            "Genres",
            f"{len(genres)}",
            "Model Features",
            "🎬",
        )

    with c3:
        metric_card(
            "Countries",
            f"{len(countries)}",
            "Geographic Features",
            "🌍",
        )

    with c4:
        metric_card(
            "Devices",
            f"{len(devices)}",
            "Behaviour Signals",
            "📱",
        )

    st.divider()

    left, right = st.columns(2)

    with left:

        fig = px.bar(
            quality,
            x="quality",
            y="avg_watch_seconds",
            color="quality",
            template="plotly_dark",
            title="Average Watch Time by Streaming Quality",
        )

        fig.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font=dict(color="white"),
            coloraxis_showscale=False,
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        fig = px.scatter(
            genres,
            x="avg_rating",
            y="completion",
            size="views",
            hover_name="genre",
            template="plotly_dark",
            title="Genre Behaviour Features",
        )

        fig.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font=dict(color="white"),
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.info(
        """
### 🚀 Upcoming ML Models

- Customer Churn Prediction
- Recommendation Engine (ALS)
- Watch Time Forecasting
- Content Popularity Prediction
- Subscriber Lifetime Value
- Anomaly Detection
"""
    )