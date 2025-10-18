import streamlit as st
from common.footer import show_footer
st.set_page_config(
    page_icon="💻",
    layout="centered"
)
#pg = st.navigation([st.Page("pages/Главная.py"),
#                        st.Page("pages/1_Параметры_влажного_воздуха.py"), 
#                        st.Page("pages/2_Плотность_сухого_воздуха.py")])

pg = st.navigation(
    {       "": [st.Page("pages/Главная.py", default=True)],
            "Воздух": [st.Page("pages/1_Параметры_влажного_воздуха.py"), 
                       st.Page("pages/1_Плотность_сухого_воздуха.py"),
                       st.Page("pages/1_Вязкость_сухого_воздуха.py")],
            "Вода/пар": [st.Page("pages/2_Свойства_воды.py"), 
                         st.Page("pages/2_Свойства_перегретого_пара.py")],       
            "Гидравлика": [st.Page("pages/3_Кавитационный запас.py")]
            
        }
)



pg.run()
show_footer()   