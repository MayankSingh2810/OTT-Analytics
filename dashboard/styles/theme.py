import streamlit as st


def apply_theme():

    st.markdown(
        """
<style>

/* ==========================================================
GLOBAL
========================================================== */

html, body, [class*="css"]{
    font-family:Inter,sans-serif;
}

.stApp{
    background:#0B1220;
}

/* ==========================================================
PAGE
========================================================== */

.block-container{

    max-width:1550px;

    padding-top:1.4rem;

    padding-left:2rem;

    padding-right:2rem;

}

/* ==========================================================
SIDEBAR
========================================================== */

section[data-testid="stSidebar"]{

    background:#0F172A;

    border-right:1px solid rgba(56,189,248,.15);

    width:310px !important;

}

/* Sidebar text */

section[data-testid="stSidebar"] *{

    color:white !important;

}

/* ==========================================================
HEADINGS
========================================================== */

h1{

    color:white;

    font-size:42px;

    font-weight:800;

}

h2{

    color:white;

}

h3{

    color:#E2E8F0;

}

/* ==========================================================
METRIC CARDS
========================================================== */

div[data-testid="metric-container"]{

    background:#151D2A;

    border-radius:18px;

    border:1px solid rgba(56,189,248,.18);

    padding:20px;

    box-shadow:
        0 10px 28px rgba(0,0,0,.35);

}

/* ==========================================================
DATAFRAMES
========================================================== */

div[data-testid="stDataFrame"]{

    border-radius:18px;

    border:1px solid rgba(56,189,248,.12);

    overflow:hidden;

}

/* ==========================================================
SUCCESS / INFO
========================================================== */

div[data-baseweb="notification"]{

    border-radius:16px;

}

/* ==========================================================
BUTTONS
========================================================== */

.stButton>button{

    border:none;

    border-radius:12px;

    background:#38BDF8;

    color:white;

    font-weight:600;

}

.stButton>button:hover{

    background:#0EA5E9;

    color:white;

}

/* ==========================================================
DIVIDERS
========================================================== */

hr{

    margin-top:28px;

    margin-bottom:28px;

    border:none;

    border-top:1px solid rgba(255,255,255,.08);

}

/* ==========================================================
SCROLLBAR
========================================================== */

::-webkit-scrollbar{

    width:10px;

}

::-webkit-scrollbar-thumb{

    background:#334155;

    border-radius:10px;

}

::-webkit-scrollbar-track{

    background:#0B1220;

}

</style>
""",
        unsafe_allow_html=True,
    )