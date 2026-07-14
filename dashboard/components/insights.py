import streamlit as st


def executive_insights(row):

    st.subheader("🧠 Executive AI Insights")

    c1, c2 = st.columns(2)

    with c1:

        st.info(
            f"""
Average Watch Time

{row['avg_watch_minutes']:.2f} minutes

Users spend considerable time on the platform.
"""
        )

        st.info(
            f"""
Completion Rate

{row['completion_rate']*100:.2f}%

Content completion is healthy.
"""
        )

    with c2:

        st.info(
            f"""
Like Rate

{row['like_rate']*100:.2f}%

Positive engagement remains strong.
"""
        )

        st.info(
            f"""
Binge Watch Rate

{row['binge_watch_rate']*100:.2f}%

Excellent binge consumption.
"""
        )

def pipeline_status():

    st.subheader("🚀 Platform Health")

    c1, c2, c3, c4 = st.columns(4)

    c1.success("Bronze ✓")
    c2.success("Silver ✓")
    c3.success("Gold ✓")
    c4.success("Streaming ✓")