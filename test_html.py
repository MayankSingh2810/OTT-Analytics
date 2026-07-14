import streamlit as st

st.set_page_config(layout="wide")

st.markdown(
    """
<div style="background:red;padding:30px;border-radius:20px;color:white;">
    <h1>Hello World</h1>
    <div class="metric-card">
        <div class="metric-icon">💰</div>
        <div class="metric-title">Revenue</div>
        <div class="metric-value">₹50M</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)