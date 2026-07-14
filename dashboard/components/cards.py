import streamlit as st


def metric_card(title, value, delta=None):

    with st.container(border=True):

        st.caption(title)

        st.markdown(
            f"""
            <h2 style="margin-bottom:0px;">
                {value}
            </h2>
            """,
            unsafe_allow_html=True,
        )

        if delta is not None:
            if str(delta).startswith("-"):
                st.error(delta)
            else:
                st.success(delta)