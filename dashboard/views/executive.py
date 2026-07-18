import streamlit as st

from utils.live_data import load_table

from components.insights import (
    executive_insights,
    pipeline_status,
)


def show():

    dashboard = load_table("dashboard_summary")

    st.title("🎬 OTT Stream Intelligence")
    st.caption(
        "Enterprise Big Data Analytics Platform"
    )

    if dashboard.empty:
        st.error("Dashboard Summary not found.")
        return

    row = dashboard.iloc[0]

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🎥 Watch Hours",
        f"{row['watch_hours']:,.0f}"
    )

    c2.metric(
        "👥 Registered Users",
        f"{int(row['registered_users']):,}"
    )

    c3.metric(
        "📺 Content Library",
        f"{int(row['content_library']):,}"
    )

    c4.metric(
        "⭐ Avg Completion",
        f"{row['avg_completion']:.2f}%"
    )

    st.markdown("---")

    c1, c2 = st.columns([2, 1])

    with c1:

        st.subheader("Platform Overview")

        overview = {
            "Metric": [
                "Total Events",
                "Unique Users",
                "Unique Content",
                "Average Watch Time",
                "Completion Rate",
                "Like Rate",
                "Binge Watch Rate",
            ],
            "Value": [
                f"{int(row['total_events']):,}",
                f"{int(row['unique_users']):,}",
                f"{int(row['unique_content']):,}",
                f"{row['avg_watch_minutes']:.2f} min",
                f"{row['completion_rate']*100:.2f}%",
                f"{row['like_rate']*100:.2f}%",
                f"{row['binge_watch_rate']*100:.2f}%",
            ],
        }

        st.dataframe(
            overview,
            use_container_width=True,
            hide_index=True,
        )

    with c2:

        pipeline_status()

    st.markdown("---")

    executive_insights(row)