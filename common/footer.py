import streamlit as st

def show_footer():
    st.markdown(
        """
        <hr>
        <p style="text-align: left; color: gray;">
        <small>
        © 2025 С.В. Медведев. E-mail: engpython@yandex.ru
        </small>
        </p>
        """,
        unsafe_allow_html=True
    )