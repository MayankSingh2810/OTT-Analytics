import streamlit as st

def sidebar():

    st.sidebar.title("OTT Stream Intelligence")
    st.sidebar.caption("Enterprise Analytics Platform")

    st.sidebar.divider()

    page = st.sidebar.radio(
        "Navigation",
        [
            "Executive Dashboard",
            "Content Analytics",
            "User Analytics",
            "Revenue Analytics",
            "ML Predictions",
            "Real-Time Monitoring",
        ]
    )

    st.sidebar.divider()

    st.sidebar.subheader("System Status")

    st.sidebar.success("Pipeline Healthy")

    st.sidebar.caption("Last Refresh")
    st.sidebar.write("Today")

    st.sidebar.divider()

    st.sidebar.subheader("Data Lake")

    st.sidebar.write("Bronze")
    st.sidebar.write("Silver")
    st.sidebar.write("Gold")
    st.sidebar.write("Feature Store")

    st.sidebar.divider()

    st.sidebar.subheader("Machine Learning")

    st.sidebar.write("Random Forest")
    st.sidebar.write("Gradient Boosted Trees")
    st.sidebar.write("ARIMA Forecast")
    st.sidebar.write("ALS Recommendation")

    return page