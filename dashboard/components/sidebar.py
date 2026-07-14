import streamlit as st


def sidebar():

    st.sidebar.title("🎬 OTT Intelligence")

    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Executive Dashboard",
            "📺 Content Analytics",
            "👥 User Analytics",
            "💰 Revenue Analytics",
            "🤖 ML Predictions",
            "⚡ Real-Time Monitoring",
        ]
    )

    st.sidebar.markdown("---")

    st.sidebar.success("Pipeline Running")

    st.sidebar.caption("Bronze ✓")
    st.sidebar.caption("Silver ✓")
    st.sidebar.caption("Gold ✓")

    return page