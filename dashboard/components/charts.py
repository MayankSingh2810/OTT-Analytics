import plotly.express as px
import streamlit as st
import pandas as pd


def line_chart(df, x, y, title=""):

    fig = px.line(
        df,
        x=x,
        y=y,
        title=title,
        markers=True,
        template="plotly_dark",
    )

    fig.update_layout(
        height=380,
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def bar_chart(df, x, y, title):

    if isinstance(df, dict):
        df = pd.DataFrame(df)

    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        template="plotly_dark"
    )

    fig.update_layout(
        height=380,
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
def pie_chart(df, names, values, title):

    if isinstance(df, dict):
        df = pd.DataFrame(df)

    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.55,
        title=title,
        template="plotly_dark"
    )

    fig.update_layout(
        height=380,
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )