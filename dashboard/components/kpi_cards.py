import streamlit as st


def metric_card(
    title,
    value,
    delta=None,
    help_text=None
):
    """
    Reusable KPI Card

    Parameters
    ----------
    title : str
    value : str/int/float
    delta : str/int/float
    help_text : str
    """

    st.metric(
        label=title,
        value=value,
        delta=delta,
        help=help_text,
        border=True
    )