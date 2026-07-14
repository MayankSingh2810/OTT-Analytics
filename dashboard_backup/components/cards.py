import streamlit as st


# ==========================================================
# NETFLIX KPI CARD
# ==========================================================

def metric_card(
    title,
    value,
    subtitle="",
    icon="📊",
    color="#E50914"
):
    st.markdown(
        f"""
        <style>
        .metric-card {{
            background: linear-gradient(145deg,#161B22,#0E1117);
            border:1px solid rgba(255,255,255,.08);
            border-left:6px solid {color};
            border-radius:18px;
            padding:18px;
            height:175px;
            transition:.25s;
            box-shadow:0 0 25px rgba(0,0,0,.35);
        }}

        .metric-card:hover {{
            transform:translateY(-6px);
            box-shadow:0 0 30px rgba(229,9,20,.30);
            border-left:6px solid #FF4B4B;
        }}

        .metric-title {{
            color:#9CA3AF;
            font-size:14px;
            font-weight:500;
            margin-bottom:8px;
        }}

        .metric-value {{
            color:white;
            font-size:34px;
            font-weight:700;
            margin-top:8px;
            margin-bottom:6px;
        }}

        .metric-sub {{
            color:#00E676;
            font-size:14px;
            font-weight:500;
        }}

        .metric-icon {{
            font-size:34px;
            margin-bottom:12px;
        }}
        </style>

        <div class="metric-card">

            <div class="metric-icon">
                {icon}
            </div>

            <div class="metric-title">
                {title}
            </div>

            <div class="metric-value">
                {value}
            </div>

            <div class="metric-sub">
                {subtitle}
            </div>

        </div>

        """,
        unsafe_allow_html=True
    )


# ==========================================================
# STATUS CARD
# ==========================================================

def status_card(title, status, icon="🟢"):

    colors = {
        "Healthy": "#00C853",
        "Running": "#00C853",
        "Warning": "#FFA726",
        "Stopped": "#E53935",
        "Offline": "#E53935",
    }

    color = colors.get(status, "#2196F3")

    st.markdown(
        f"""
        <div style="
            background:#161B22;
            padding:18px;
            border-radius:16px;
            border-left:6px solid {color};
            box-shadow:0 0 18px rgba(0,0,0,.30);
            margin-bottom:10px;
        ">

        <h4 style="color:white;margin:0;">
            {icon} {title}
        </h4>

        <p style="
            color:{color};
            margin-top:10px;
            font-size:18px;
            font-weight:700;
        ">
            {status}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# SECTION HEADER
# ==========================================================

def section_header(title, subtitle=""):

    st.markdown(
        f"""
        <div style="margin-top:10px;margin-bottom:15px;">

        <h2 style="
            color:white;
            margin-bottom:0;
        ">
            {title}
        </h2>

        <p style="
            color:#9CA3AF;
            margin-top:4px;
        ">
            {subtitle}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# ALERT CARD
# ==========================================================

def alert_card(message):

    st.markdown(
        f"""
        <div style="
            background:#2A1111;
            border-left:6px solid #E50914;
            border-radius:12px;
            padding:18px;
            margin-top:12px;
            margin-bottom:12px;
        ">

        <span style="
            color:white;
            font-size:16px;
        ">
        🚨 {message}
        </span>

        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# SUCCESS CARD
# ==========================================================

def success_card(message):

    st.markdown(
        f"""
        <div style="
            background:#0F2A18;
            border-left:6px solid #00C853;
            border-radius:12px;
            padding:18px;
            margin-top:12px;
            margin-bottom:12px;
        ">

        <span style="
            color:white;
            font-size:16px;
        ">
        ✅ {message}
        </span>

        </div>
        """,
        unsafe_allow_html=True
    )