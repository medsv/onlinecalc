import streamlit as st
from libs.calcdryairdens import calc_dryair_dens
from common.footer import show_footer
st.set_page_config(
    page_title="Расчёт плотности сухого воздуха",
    page_icon="💻",
    layout="centered"
)
# Заголовок страницы
st.title("Расчёт плотности сухого воздуха")
st.markdown("Определение плотности сухого воздуха для t = [-100; 1000] С,  p = [0,1; 20] МПа")

t = st.number_input("Температура, °С", value=20., step=1., min_value=-100., max_value=1000., key ="t", width = 200)
p = st.number_input("Давление, Па", value=101325.0, step=1., min_value=100000., max_value=20e6, key ="p", width = 200)
if st.button("Рассчитать"):
    try:
        res = calc_dryair_dens(t, p)
        result = f"Плотность {res[0]} кг/м<sup>3</sup> \n\n Коэффициент сжимаемости {res[1]}".replace(".", ",")
        st.markdown(result, unsafe_allow_html=True)

    except Exception as e:
        #st.markdown(f":orange-badge[⚠️ {str(e)}]")
        st.error(f"{str(e)}", icon="⚠️")

with st.expander("Дополнительно"):
    st.markdown("[Плотность сухого воздуха](https://dzen.ru/a/XzUUMppesQVXBAwF)")

show_footer()