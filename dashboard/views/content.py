import streamlit as st
import plotly.express as px

from utils.live_data import load_table
from components.cards import metric_card
from components.charts import style_fig


def show():

    st.title("📺 Content Analytics")
    st.caption("Enterprise OTT Content Intelligence")

    content = load_table("content")
    top = load_table("top_content")
    genre = load_table("genre_analytics")

    if content.empty or top.empty or genre.empty:
        st.error("Content tables not found in MySQL.")
        return

    # --------------------------
    # Fix numeric columns
    # --------------------------

    numeric_cols = [
        "views",
        "avg_rating",
        "avg_watch_minutes",
        "avg_completion",
        "watch_hours",
        "unique_viewers",
        "imdb_rating",
        "total_views",
        "avg_imdb_rating",
    ]

    for df in [content, top, genre]:
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].astype(float)

    # Sort genre by total_views (highest to lowest) so it's consistent everywhere
    if "total_views" in genre.columns:
        genre = genre.sort_values("total_views", ascending=False)

    st.info(
        """
### Content Intelligence

Monitor genre popularity, viewing behaviour,
content performance and audience engagement
across the OTT platform.
"""
    )

    st.subheader("Content Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("Content Catalog", f"{len(content):,}")

    with c2:
        if "genre" in genre.columns:
            metric_card("Genre Categories", f"{genre['genre'].nunique()}")
        else:
            metric_card("Genre Categories", "N/A")

    with c3:
        if "views" in top.columns:
            metric_card("Total Platform Views", f"{int(top['views'].sum()):,}")
        else:
            metric_card("Total Platform Views", "N/A")

    with c4:
        if "avg_rating" in content.columns:
            metric_card("Average IMDb Rating", f"{content['avg_rating'].mean():.2f}")
        else:
            metric_card("Average IMDb Rating", "N/A")

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("🎭 Views by Genre")

        if {"genre", "total_views"}.issubset(genre.columns):

            fig = px.bar(
                genre,
                x="genre",
                y="total_views",
                color="total_views",
                template="plotly_white"
            )

            fig = style_fig(fig)

            st.plotly_chart(fig, use_container_width=True)

    with right:

        st.subheader("⭐ Average Rating by Genre")

        if {"genre", "avg_imdb_rating"}.issubset(genre.columns):

            fig = px.bar(
                genre.sort_values("avg_imdb_rating"),
                x="avg_imdb_rating",
                y="genre",
                orientation="h",
                color="avg_imdb_rating",
                template="plotly_white"
            )

            fig = style_fig(fig)

            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("🔥 Top Content")

    top10 = None

    if "views" in top.columns:

        top10 = top.sort_values(
            "views",
            ascending=False
        ).head(10)

        fig = px.bar(
            top10,
            x="views",
            y="title",
            orientation="h",
            color="views",
            template="plotly_white"
        )

        fig = style_fig(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    left, right = st.columns(2)

    with left:

        if "avg_rating" in content.columns:

            st.subheader("IMDb Rating Distribution")

            fig = px.histogram(
                content,
                x="avg_rating",
                nbins=20,
                template="plotly_white"
            )

            fig = style_fig(fig)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with right:

        if {"avg_watch_minutes", "avg_completion"}.issubset(content.columns):

            st.subheader("Watch Time vs Completion")

            color = "genre" if "genre" in content.columns else None

            fig = px.scatter(
                content,
                x="avg_watch_minutes",
                y="avg_completion",
                color=color,
                template="plotly_white"
            )

            fig.update_traces(
                marker=dict(size=9)
            )

            fig = style_fig(fig)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.divider()

    st.subheader("Top Content Dataset")

    available = [
        c for c in [
            "title",
            "genre",
            "content_type",
            "views",
            "unique_viewers",
            "watch_hours",
            "imdb_rating",
        ]
        if c in top.columns
    ]

    with st.container(border=True):
        st.dataframe(
            top[available],
            use_container_width=True,
            height=420
        )

    st.divider()

    st.subheader("🧠 Content Insights")

    c1, c2 = st.columns(2)

    with c1:
        if "genre" in genre.columns and len(genre) > 0:
            st.info(
                f"""
Top Genre

**{genre.iloc[0]['genre']}**

This genre contributes the highest platform engagement.
"""
            )

    with c2:
        if top10 is not None and "title" in top10.columns and len(top10) > 0:
            st.info(
                f"""
Most Watched Title

**{top10.iloc[0]['title']}**

Highest performing content across the platform.
"""
            )