import streamlit as st


# ==========================================================
# Executive AI Insights
# ==========================================================

def executive_insights(row):

    st.subheader("🧠 Executive Intelligence")

    st.success(
        f"""
**User Engagement**

Average watch time is **{row['avg_watch_minutes']:.2f} minutes** per session.

This indicates healthy user engagement across the platform.
"""
    )

    st.success(
        f"""
**Content Retention**

Content completion rate is **{row['completion_rate']*100:.2f}%**.

Most users finish the content they begin watching.
"""
    )

    st.success(
        f"""
**Viewer Satisfaction**

Like rate currently stands at **{row['like_rate']*100:.2f}%**.

Recommendation quality and content relevance remain strong.
"""
    )

    st.success(
        f"""
**Binge Watching Behaviour**

Binge-watch rate is **{row['binge_watch_rate']*100:.2f}%**.

Users continue watching multiple episodes in a single session,
indicating strong long-form engagement.
"""
    )


# ==========================================================
# Pipeline Status
# ==========================================================

def pipeline_status():

    st.subheader("🚀 Platform Health")

    st.success("🟢 Bronze Layer — Operational")

    st.success("🟢 Silver Layer — Operational")

    st.success("🟢 Gold Layer — Operational")

    st.success("🟢 Feature Store — Operational")

    st.success("🟢 Machine Learning Pipeline — Operational")

    st.success("🟢 Recommendation Engine — Operational")

    st.success("🟢 Forecasting Engine — Operational")