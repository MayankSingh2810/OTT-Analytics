import pandas as pd
import plotly.express as px
import streamlit as st


BACKGROUND = "#0f172a"
ACCENT = "#38bdf8"


def style_fig(fig):

    fig.update_layout(

        height=420,

        margin=dict(
            l=20,
            r=20,
            t=45,
            b=20
        ),

        paper_bgcolor=BACKGROUND,
        plot_bgcolor=BACKGROUND,

        font=dict(
            family="Inter",
            size=14,
            color="#e2e8f0"
        ),

        title_x=0.02,

        hovermode="x unified",

        legend=dict(
            orientation="h",
            y=1.08,
            x=0
        ),

        xaxis=dict(
            showgrid=False,
            zeroline=False
        ),

        yaxis=dict(
            gridcolor="#334155",
            zeroline=False
        )
    )

    return fig


def _style(fig, title):

    fig = style_fig(fig)

    fig.update_layout(

        title=dict(
            text=title,
            x=0.02,
            font=dict(
                size=20,
                color="white"
            )
        ),

        height=380,

        margin=dict(
            l=20,
            r=20,
            t=55,
            b=20
        ),

        legend=dict(
            font=dict(size=12)
        )
    )

    return fig


def line_chart(df, x, y, title=""):

    fig = px.line(
        df,
        x=x,
        y=y,
        markers=True,
        template="plotly_dark"
    )

    fig.update_traces(
        line=dict(width=3, color=ACCENT),
        marker=dict(size=7, color=ACCENT)
    )

    fig = _style(fig, title)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def bar_chart(df, x, y, title=""):

    if isinstance(df, dict):
        df = pd.DataFrame(df)

    fig = px.bar(
        df,
        x=x,
        y=y,
        template="plotly_dark"
    )

    fig.update_traces(
        marker=dict(color=ACCENT),
        marker_line_width=0
    )

    fig = _style(fig, title)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def pie_chart(df, names, values, title=""):

    if isinstance(df, dict):
        df = pd.DataFrame(df)

    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.62,
        template="plotly_dark"
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig = _style(fig, title)

    st.plotly_chart(
        fig,
        use_container_width=True
    )