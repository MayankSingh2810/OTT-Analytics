import streamlit as st


def sidebar():

    with st.sidebar:

        st.markdown(
            """
            <div style="text-align:center;padding-bottom:10px;">
                <h1 style="margin-bottom:0;color:#E50914;">
                    🎬 OTT
                </h1>
                <h3 style="margin-top:0;">
                    Stream Intelligence
                </h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        page = st.radio(

            "Navigation",

            [

                "🏠 Executive Dashboard",

                "📺 Content Analytics",

                "👥 User Analytics",

                "💰 Revenue Analytics",

                "🤖 ML Predictions",

                "⚡ Real-Time Monitoring",

            ],

            label_visibility="collapsed",

        )

        st.markdown("---")

        st.markdown("### 🚀 Platform")

        col1, col2 = st.columns(2)

        with col1:

            st.metric("Bronze", "✓")

            st.metric("Silver", "✓")

            st.metric("Gold", "✓")

        with col2:

            st.metric("MySQL", "✓")

            st.metric("Spark", "✓")

            st.metric("Streaming", "Live")

        st.markdown("---")

        st.markdown("### 📊 Pipeline")

        st.progress(100)

        st.caption("Bronze → Silver → Gold → MySQL → Dashboard")

        st.markdown("---")

        st.markdown("### ⚙️ System")

        st.success("Spark Connected")

        st.success("MySQL Connected")

        st.success("Dashboard Online")

        st.markdown("---")

        st.caption(
            """
            OTT Stream Intelligence

            Enterprise Analytics Platform

            Version 3.0
            """
        )

    return page