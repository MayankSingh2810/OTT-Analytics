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
        st.error("Gold Layer tables not found.")
        return

    # ==========================================================
    # KPI SECTION
    # ==========================================================

    st.subheader("Content Overview")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Titles",
            f"{len(content):,}"
        )

    with c2:
        metric_card(
            "Genres",
            f"{genre.genre.nunique()}"
        )

    with c3:
        metric_card(
            "Total Views",
            f"{int(content.views.sum()):,}"
        )

    with c4:
        metric_card(
            "Average Rating",
            f"{content.avg_rating.mean():.2f}"
        )

    st.divider()

    # ==========================================================
    # GENRE ANALYTICS
    # ==========================================================

    left, right = st.columns(2)

    with left:

        st.subheader("🎭 Views by Genre")

        fig = px.bar(

            genre,

            x="genre",

            y="total_views",

            color="total_views",

            template="plotly_dark"

        )

        fig.update_layout(

            height=420,

            paper_bgcolor="#0d1117",

            plot_bgcolor="#0d1117",

            coloraxis_showscale=False

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("⏱ Watch Hours by Genre")

        fig = px.pie(

            genre,

            names="genre",

            values="total_watch_hours",

            hole=.55,

            template="plotly_dark"

        )

        fig.update_layout(

            height=420,

            paper_bgcolor="#0d1117"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ==========================================================
    # TOP CONTENT
    # ==========================================================

    st.subheader("🔥 Top 20 Performing Content")

    top20 = top.sort_values(

        "views",

        ascending=False

    ).head(20)

    fig = px.bar(

        top20,

        x="views",

        y="title",

        orientation="h",

        color="imdb_rating",

        template="plotly_dark"

    )

    fig.update_layout(

        height=650,

        paper_bgcolor="#0d1117",

        plot_bgcolor="#0d1117",

        yaxis=dict(categoryorder="total ascending")

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # ==========================================================
    # RATINGS
    # ==========================================================

    left, right = st.columns(2)

    with left:

        st.subheader("⭐ IMDb Rating Distribution")

        fig = px.histogram(

            content,

            x="avg_rating",

            nbins=20,

            template="plotly_dark"

        )

        fig.update_layout(

            paper_bgcolor="#0d1117",

            plot_bgcolor="#0d1117",

            height=400

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with right:

        st.subheader("📈 Average Watch Time")

        fig = px.scatter(

            content,

            x="avg_watch_minutes",

            y="avg_completion",

            color="genre",

            template="plotly_dark"

        )

        fig.update_layout(

            paper_bgcolor="#0d1117",

            plot_bgcolor="#0d1117",

            height=400

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()

    # ==========================================================
    # ENTERPRISE TABLE
    # ==========================================================

    st.subheader("📋 Top Content Dataset")

    st.dataframe(

        top[[
            "title",
            "genre",
            "content_type",
            "views",
            "unique_viewers",
            "watch_hours",
            "imdb_rating"
        ]],

        use_container_width=True,

        height=450

    )

    st.success("Content Analytics Loaded Successfully")