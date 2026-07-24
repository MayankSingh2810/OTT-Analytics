import streamlit as st


def metric_card(title, value, delta=None):

    with st.container(border=True):

        st.caption(title)

        st.subheader(str(value))

        if delta is not None:

            if str(delta).startswith("-"):
                st.error(str(delta))
            else:
                st.success(str(delta))