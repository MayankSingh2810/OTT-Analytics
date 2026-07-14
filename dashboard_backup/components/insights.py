import streamlit as st


def executive_insights(
    revenue,
    watch,
    devices,
    content,
):

    st.subheader("🧠 Executive Insights")

    c1, c2 = st.columns(2)

    with c1:

        st.success(
            f"""
### 💰 Revenue

Monthly Revenue

**₹{revenue['monthly_revenue'].iloc[0]:,.0f}**

Average Plan Price

**₹{revenue['average_plan_price'].iloc[0]:.2f}**
"""
        )

        st.info(
            f"""
### 👥 Subscribers

Active Subscribers

**{revenue['active_subscribers'].iloc[0]:,}**

Auto Renew

**{revenue['auto_renew_users'].iloc[0]:,}**
"""
        )

        top = content.iloc[0]

        st.warning(
            f"""
### 🎬 Top Content

**{top['title']}**

⭐ IMDb : {top['imdb_rating']}

👀 Views : {top['total_views']}

🎯 Completion : {top['avg_completion']:.2f}%
"""
        )

    with c2:

        device = devices.sort_values(
            "usage_percent",
            ascending=False,
        ).iloc[0]

        st.info(
            f"""
### 📺 Most Used Device

**{device['device']}**

Usage Share

**{device['usage_percent']:.2f}%**
"""
        )

        st.success(
            f"""
### ⏱ Watch Behaviour

Total Watch Hours

**{watch['total_watch_hours'].iloc[0]:,.0f}**

Average Completion

**{watch['avg_completion_pct'].iloc[0]:.2f}%**
"""
        )

        st.error(
            """
### 🚀 Recommendation

Increase investment in

✔ High Completion Titles

✔ Smart TV Experience

✔ Auto Renewal Campaigns

to maximize revenue.
"""
        )