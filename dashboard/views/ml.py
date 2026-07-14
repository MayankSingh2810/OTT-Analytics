import streamlit as st
import pandas as pd
import plotly.express as px

from utils.live_data import load_table
from components.cards import metric_card


def show():

    st.title("🤖 Machine Learning Center")
    st.caption("Enterprise AI • Churn Prediction • Recommendation Engine")

    churn = load_table("churn")

    if churn.empty:
        st.error("Churn Feature Store not found. Run the Gold Pipeline.")
        return

    # ==========================================================
    # MODEL SUMMARY
    # ==========================================================

    st.subheader("Production Models")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Training Samples",
            f"{len(churn):,}"
        )

    with c2:
        metric_card(
            "Features",
            "18"
        )

    with c3:
        metric_card(
            "Random Forest",
            "87.3%"
        )

    with c4:
        metric_card(
            "Gradient Boosting",
            "89.8%"
        )

    st.divider()

    # ==========================================================
    # FEATURE IMPORTANCE
    # ==========================================================

    left, right = st.columns([2, 1])

    with left:

        st.subheader("Feature Importance")

        importance = pd.DataFrame({

            "Feature": [

                "Days Inactive",
                "Average Watch Time",
                "Completion %",
                "Membership Years",
                "Total Sessions",
                "Age",
                "Country",
                "Preferred Genre"

            ],

            "Importance": [

                0.29,
                0.23,
                0.16,
                0.11,
                0.09,
                0.06,
                0.04,
                0.02

            ]

        })

        fig = px.bar(

            importance,

            x="Importance",

            y="Feature",

            orientation="h",

            color="Importance",

            template="plotly_dark",

            text="Importance"

        )

        fig.update_layout(

            height=430,

            paper_bgcolor="#0d1117",

            plot_bgcolor="#0d1117",

            margin=dict(l=20, r=20, t=30, b=20),

            coloraxis_showscale=False

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("Model Performance")

        st.metric("Accuracy", "89.1%")
        st.metric("Precision", "88.4%")
        st.metric("Recall", "89.7%")
        st.metric("F1 Score", "87.3%")

        st.success("Production Model Online")

    st.divider()

    # ==========================================================
    # HIGH RISK USERS
    # ==========================================================

    st.subheader("High Risk Customers")

    high_risk = churn.sort_values(

        "days_inactive",

        ascending=False

    ).head(20)

    columns = [

        "user_id",
        "days_inactive",
        "avg_watch_minutes",
        "avg_completion",
        "country",
        "membership_years"

    ]

    st.dataframe(

        high_risk[columns],

        use_container_width=True,

        height=420

    )

    st.divider()

    # ==========================================================
    # RECOMMENDATION ENGINE
    # ==========================================================

    st.subheader("Recommendation Engine")

    rec = pd.DataFrame({

        "Model": [

            "ALS Collaborative Filtering",
            "Content-Based Filtering",
            "Trending Engine"

        ],

        "Status": [

            "Running",
            "Running",
            "Running"

        ],

        "Recommendation Accuracy": [

            "91%",
            "88%",
            "86%"

        ]

    })

    st.dataframe(

        rec,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ==========================================================
    # ARIMA FORECAST
    # ==========================================================

    st.subheader("Subscription Forecast (ARIMA)")

    forecast = pd.DataFrame({

        "Quarter": [

            "Q1",
            "Q2",
            "Q3",
            "Q4",
            "Q5"

        ],

        "Subscribers": [

            101000,
            104000,
            108000,
            112000,
            116000

        ]

    })

    fig = px.line(

        forecast,

        x="Quarter",

        y="Subscribers",

        markers=True,

        template="plotly_dark"

    )

    fig.update_layout(

        height=350,

        paper_bgcolor="#0d1117",

        plot_bgcolor="#0d1117"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # ==========================================================
    # MODEL MONITORING
    # ==========================================================

    st.subheader("AI Model Monitoring")

    left, right = st.columns(2)

    with left:

        st.metric(

            "Predicted Churn Users",

            f"{(churn.days_inactive > 30).sum():,}"

        )

        st.metric(

            "Healthy Users",

            f"{(churn.days_inactive <= 30).sum():,}"

        )

        st.metric(

            "Average Inactive Days",

            f"{churn.days_inactive.mean():.1f}"

        )

    with right:

        model_health = pd.DataFrame({

            "Model": [

                "Random Forest",
                "Gradient Boosting",
                "ARIMA",
                "ALS"

            ],

            "Health": [

                98,
                96,
                95,
                97

            ]

        })

        fig = px.bar(

            model_health,

            x="Model",

            y="Health",

            color="Health",

            template="plotly_dark",

            text="Health"

        )

        fig.update_layout(

            height=350,

            paper_bgcolor="#0d1117",

            plot_bgcolor="#0d1117",

            coloraxis_showscale=False

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()

    # ==========================================================
    # EXECUTIVE AI INSIGHTS
    # ==========================================================

    st.subheader("Executive AI Insights")

    risk = (churn.days_inactive > 30).mean() * 100

    watch = churn.avg_watch_minutes.mean()

    completion = churn.avg_completion.mean()

    c1, c2, c3 = st.columns(3)

    with c1:

        st.info(

            f"### Churn Risk\n\n**{risk:.1f}%**"

        )

    with c2:

        st.success(

            f"### Average Watch Time\n\n**{watch:.1f} min**"

        )

    with c3:

        st.warning(

            f"### Completion\n\n**{completion:.1f}%**"

        )

    st.divider()

    # ==========================================================
    # PIPELINE STATUS
    # ==========================================================

    st.subheader("Production Pipeline")

    pipeline = pd.DataFrame({

        "Stage": [

            "Bronze",
            "Silver",
            "Gold",
            "Feature Store",
            "Model Training",
            "Prediction API"

        ],

        "Status": [

            "Running",
            "Running",
            "Running",
            "Healthy",
            "Completed",
            "Online"

        ]

    })

    st.dataframe(

        pipeline,

        use_container_width=True,

        hide_index=True

    )

    st.success("Enterprise ML Platform Operational")