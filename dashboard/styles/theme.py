import streamlit as st


def apply_theme():

    st.markdown(
        """
<style>

html, body, [class*="css"]{

    font-family:Inter,sans-serif;

}

.stApp{

    background:#0d1117;

}

.block-container{

    max-width:1500px;

    padding-top:1.2rem;

    padding-left:2rem;

    padding-right:2rem;

}

section[data-testid="stSidebar"]{

    background:#111827;

    border-right:1px solid #1f2937;

}

h1{

    font-size:42px;

    font-weight:700;

    color:white;

}

h2{

    color:white;

}

h3{

    color:white;

}

div[data-testid="stMetric"]{

    background:#161b22;

    border:1px solid #2d333b;

    border-radius:18px;

    padding:20px;

}

div[data-testid="metric-container"]{

    background:#161b22;

    border-radius:18px;

    border:1px solid #2d333b;

    padding:18px;

}

hr{

    margin-top:25px;

    margin-bottom:25px;

}

</style>
""",
        unsafe_allow_html=True,
    )