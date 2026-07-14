import streamlit as st

# ==========================================================
# THEME
# ==========================================================

from styles.theme import apply_theme

# ==========================================================
# SIDEBAR
# ==========================================================

from components.sidebar import sidebar

# ==========================================================
# VIEWS
# ==========================================================

from views.executive import show as executive
from views.content import show as content
from views.users import show as users
from views.revenue import show as revenue
from views.ml import show as ml
from views.realtime import show as realtime

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(

    page_title="OTT Stream Intelligence",

    page_icon="🎬",

    layout="wide",

    initial_sidebar_state="expanded",

)

# ==========================================================
# APPLY GLOBAL THEME
# ==========================================================

apply_theme()

# ==========================================================
# SIDEBAR
# ==========================================================

page = sidebar()

# ==========================================================
# PAGE ROUTING
# ==========================================================

PAGES = {

    "🏠 Executive Dashboard": executive,

    "📺 Content Analytics": content,

    "👥 User Analytics": users,

    "💰 Revenue Analytics": revenue,

    "🤖 ML Predictions": ml,

    "⚡ Real-Time Monitoring": realtime,

}

# ==========================================================
# OPEN SELECTED PAGE
# ==========================================================

PAGES[page]()