import streamlit as st

from config import APP_TITLE

from components.sidebar import sidebar
from styles.theme import apply_theme

from views.executive import show as executive
from views.content import show as content
from views.users import show as users
from views.revenue import show as revenue
from views.ml import show as ml
from views.realtime import show as realtime


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply global styling
apply_theme()

page = sidebar()

PAGES = {
    "🏠 Executive Dashboard": executive,
    "📺 Content Analytics": content,
    "👥 User Analytics": users,
    "💰 Revenue Analytics": revenue,
    "🤖 ML Predictions": ml,
    "⚡ Real-Time Monitoring": realtime,
}

PAGES[page]()