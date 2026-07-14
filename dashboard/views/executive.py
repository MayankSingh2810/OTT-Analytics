import streamlit as st

from utils.live_data import load_table

def show():

    dashboard = load_table("dashboard")

    st.title("🎬 OTT Stream Intelligence")
    st.caption("Enterprise Big Data Analytics Platform")

    if dashboard.empty:
        st.error("Dashboard Summary not found.")
        return

    row = dashboard.iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Watch Hours",
        f"{row['watch_hours']:.1f}"
    )

    c2.metric(
        "Registered Users",
        f"{int(row['registered_users']):,}"
    )

    c3.metric(
        "Content Library",
        f"{int(row['content_library']):,}"
    )

    c4.metric(
        "Average Completion",
        f"{row['avg_completion']:.2f}%"
    )