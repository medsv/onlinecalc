import streamlit as st

def show_footer():
    st.markdown(
        """
        <hr>
        <p style="text-align: left; color: gray;">
        <small>
        Предложения/замечания/комментарии Вы можете оставить <a href ="https://dzen.ru/a/aOJcG6PWN2Lb8NUM">здесь</a><br>    
        2025 С.В. Медведев, email: engpython@yandex.ru
        </small>
        </p>
        """,
        unsafe_allow_html=True
    )