import streamlit as st
from pathlib import Path


# ==========================================================
# ENTERPRISE OTT THEME
# ==========================================================

def apply_theme():

    css_file = (
        Path(__file__).parent.parent
        / "assets"
        / "css"
        / "style.css"
    )

    if css_file.exists():

        st.markdown(
            f"<style>{css_file.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True
        )

    st.markdown(
        """
<style>

/* ==========================================================
   GOOGLE FONT
========================================================== */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');


html,
body,
[class*="css"]{

    font-family:'Inter',sans-serif;

}


/* ==========================================================
   APP
========================================================== */

.stApp{

    background:#0E1117;

    color:white;

}


/* ==========================================================
   SIDEBAR
========================================================== */

section[data-testid="stSidebar"]{

    background:#111827;

    border-right:1px solid rgba(255,255,255,.08);

}


section[data-testid="stSidebar"] *{

    color:white;

}


/* ==========================================================
   METRIC
========================================================== */

[data-testid="metric-container"]{

    background:#161B22;

    border-radius:16px;

    padding:15px;

}


/* ==========================================================
   PLOTLY
========================================================== */

.js-plotly-plot{

    border-radius:18px;

}


/* ==========================================================
   BUTTON
========================================================== */

.stButton>button{

    background:#E50914;

    color:white;

    border:none;

    border-radius:10px;

    padding:10px 24px;

    font-weight:600;

}

.stButton>button:hover{

    background:#FF4B4B;

}


/* ==========================================================
   TABS
========================================================== */

.stTabs{

    border-radius:15px;

}

.stTabs [data-baseweb="tab"]{

    color:white;

    background:#161B22;

    border-radius:10px;

}

.stTabs [aria-selected="true"]{

    background:#E50914;

}


/* ==========================================================
   DATAFRAME
========================================================== */

[data-testid="stDataFrame"]{

    border-radius:15px;

    overflow:hidden;

}


/* ==========================================================
   SUCCESS
========================================================== */

.stSuccess{

    border-radius:15px;

}


/* ==========================================================
   WARNING
========================================================== */

.stWarning{

    border-radius:15px;

}


/* ==========================================================
   ERROR
========================================================== */

.stError{

    border-radius:15px;

}


/* ==========================================================
   SCROLLBAR
========================================================== */

::-webkit-scrollbar{

    width:10px;

}

::-webkit-scrollbar-thumb{

    background:#E50914;

    border-radius:20px;

}

::-webkit-scrollbar-track{

    background:#0E1117;

}

</style>
""",
        unsafe_allow_html=True,
    )