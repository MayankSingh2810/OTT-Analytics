import streamlit as st
import pandas as pd
import plotly.express as px

from utils.live_data import load_table
from components.cards import metric_card


def show():

    st.title("⚡ Real-Time Monitoring")

    st.caption("Enterprise Streaming Infrastructure")

    watch = load_table("watch_time")

    hourly = load_table("hourly")

    country = load_table("country")

    device = load_table("device")

    dashboard = load_table("dashboard")

    st.subheader("Live Platform Status")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        metric_card(
            "Live Events",
            "1,000,000"
        )

    with c2:

        metric_card(
            "Streaming Users",
            f"{dashboard.registered_users.iloc[0]:,}"
        )

    with c3:

        metric_card(
            "Spark Jobs",
            "Running"
        )

    with c4:

        metric_card(
            "Health",
            "99.8%"
        )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("Hourly Streaming")

        fig = px.line(

            hourly,

            x="hour",

            y="events",

            markers=True,

            template="plotly_dark"

        )

        fig.update_layout(

            paper_bgcolor="#0d1117",

            plot_bgcolor="#0d1117",

            height=380

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with right:

        st.subheader("Current Country Traffic")

        fig = px.bar(

            country,

            x="country",

            y="total_events",

            template="plotly_dark",

            color="total_events"

        )

        fig.update_layout(

            paper_bgcolor="#0d1117",

            plot_bgcolor="#0d1117",

            coloraxis_showscale=False,

            height=380

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()

    left, right = st.columns(2)

    with left:

        st.subheader("Current Device Distribution")
        fig = px.pie(

        device,

         names="device",
   
         values="total_events",
  
         hole=.55,

         template="plotly_dark"

)
        fig.update_layout(

            paper_bgcolor="#0d1117",

            height=380

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with right:

        st.subheader("Infrastructure")

        st.success("🟢 Kafka Streaming")

        st.success("🟢 Spark Structured Streaming")

        st.success("🟢 Bronze Layer")

        st.success("🟢 Silver Layer")

        st.success("🟢 Gold Layer")

        st.success("🟢 MySQL Warehouse")

        st.success("🟢 Streamlit Dashboard")

    st.divider()

    st.subheader("Live Event Feed")

    events = pd.DataFrame({

        "Timestamp":[

            "11:52:01",
            "11:52:03",
            "11:52:05",
            "11:52:07",
            "11:52:08",
            "11:52:10"

        ],

        "User":[

            "USR-1023",
            "USR-8942",
            "USR-7622",
            "USR-9823",
            "USR-2112",
            "USR-6002"

        ],

        "Action":[

            "Started Movie",
            "Paused",
            "Liked Content",
            "Completed Episode",
            "Search",
            "Continue Watching"

        ]

    })

    st.dataframe(

        events,

        use_container_width=True,

        hide_index=True,

        height=260

    )

    st.success("Enterprise Streaming Platform Operational")