import streamlit as st
import plotly.express as px

from utils.live_data import load_table
from components.cards import metric_card


def show():

    st.title("📺 Content Analytics")
    st.caption("Enterprise OTT Content Intelligence")

    content = load_table("content")
    top = load_table("top_content")
    genre = load_table("genre")

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
    ]

    for df in [content, top, genre]:
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].astype(float)

    st.subheader("Content Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("Titles", f"{len(content):,}")

    with c2:
        if "genre" in genre.columns:
            metric_card("Genres", f"{genre['genre'].nunique()}")
        else:
            metric_card("Genres", "N/A")

    with c3:
        if "views" in content.columns:
            metric_card("Total Views", f"{int(content['views'].sum()):,}")
        else:
            metric_card("Total Views", "N/A")

    with c4:
        if "avg_rating" in content.columns:
            metric_card("Average Rating", f"{content['avg_rating'].mean():.2f}")
        else:
            metric_card("Average Rating", "N/A")

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("🎭 Views by Genre")

        if {"genre", "views"}.issubset(genre.columns):

            fig = px.bar(
                genre,
                x="genre",
                y="views",
                color="views",
                template="plotly_dark"
            )

            st.plotly_chart(fig, use_container_width=True)

    with right:

        st.subheader("⭐ Average Rating by Genre")

        if {"genre", "avg_rating"}.issubset(genre.columns):

            fig = px.pie(
                genre,
                names="genre",
                values="avg_rating",
                hole=.5,
                template="plotly_dark"
            )

            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("🔥 Top Content")

    if "views" in top.columns:

        top20 = top.sort_values(
            "views",
            ascending=False
        ).head(20)

        fig = px.bar(
            top20,
            x="views",
            y="title",
            orientation="h",
            color="views",
            template="plotly_dark"
        )

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
                template="plotly_dark"
            )

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
                template="plotly_dark"
            )

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

    st.dataframe(
        top[available],
        use_container_width=True,
        height=450
    )

    st.success("✅ Content Analytics Loaded Successfully")