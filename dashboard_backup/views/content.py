import streamlit as st
import plotly.express as px

from components.cards import metric_card

from utils.mysql_loader import (
    load_genre_stats,
    load_country_stats,
    load_popular_content,
)


def show():

    # ==========================================================
    # LOAD DATA
    # ==========================================================

    genre = load_genre_stats()
    countries = load_country_stats()
    content = load_popular_content()

    # ==========================================================
    # HEADER
    # ==========================================================

    st.title("🎬 Content Analytics")

    st.caption("Genre Intelligence • Content Performance • Geographic Distribution")

    st.divider()

    # ==========================================================
    # KPI CARDS
    # ==========================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Content Library",
            f"{len(content):,}",
            "Available Titles",
            "🎬",
        )

    with c2:
        metric_card(
            "Total Views",
            f"{content['views'].sum():,}",
            "Platform Views",
            "👀",
        )

    with c3:
        metric_card(
            "Average Rating",
            f"{genre['avg_rating'].mean():.2f}",
            "Across Genres",
            "⭐",
        )

    with c4:
        metric_card(
            "Avg Completion",
            f"{genre['completion'].mean():.1f}%",
            "Viewer Completion",
            "📈",
        )

    st.divider()

    # ==========================================================
    # ROW 1
    # ==========================================================

    left, right = st.columns(2)

    with left:

        fig = px.bar(
            genre,
            x="genre",
            y="views",
            color="views",
            template="plotly_dark",
            color_continuous_scale="Reds",
            title="Genre Popularity",
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
            genre,
            x="avg_rating",
            y="completion",
            size="views",
            hover_name="genre",
            template="plotly_dark",
            title="Rating vs Completion",
        )

        fig.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font=dict(color="white"),
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ==========================================================
    # COUNTRY DISTRIBUTION
    # ==========================================================

    fig = px.bar(
        countries,
        x="country",
        y="total_events",
        color="avg_watch_seconds",
        template="plotly_dark",
        title="Streaming Activity by Country",
    )

    fig.update_layout(
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="white"),
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ==========================================================
    # TOP CONTENT
    # ==========================================================

    st.subheader("🔥 Most Viewed Content")

    fig = px.bar(
        content.sort_values("views", ascending=False).head(20),
        x="views",
        y="content_id",
        orientation="h",
        color="views",
        text="views",
        template="plotly_dark",
        color_continuous_scale="Reds",
    )

    fig.update_layout(
        height=650,
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="white"),
        yaxis=dict(categoryorder="total ascending"),
        coloraxis_showscale=False,
    )

    st.plotly_chart(fig, use_container_width=True)