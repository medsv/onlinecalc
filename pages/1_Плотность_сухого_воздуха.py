import streamlit as st
from libs.calcdryairdens import calc_dryair_dens
from common.footer import show_footer
from common.print_result import print_result
from common.streamlit_components import create_unit_input, get_si_value

st.set_page_config(
    page_title="Расчёт плотности сухого воздуха",
)
# Заголовок страницы
st.title("Расчёт плотности сухого воздуха")
st.markdown("Допустимые значения входных параметров: t = [-100; 1000] °С,  p = [0,1; 20] МПа.")

t_v, t_u = create_unit_input(
        label="Температура",
        category="temperature",
        key="t",
        value=20.,
        step=1.,
        unit="°C"
        )

p_v, p_u = create_unit_input(
        label="Абсолютное давление",
        category="pressure",
        key="p",
        value=101325.0,
        step=1.,
        unit="Па"
        )

#t: float = st.number_input("Температура, °С", value=20., step=1., min_value=-100., max_value=1000., key ="t", width = 200)
#p: float = st.number_input("Абсолютное давление, Па", value=101325.0, step=1., min_value=100000., max_value=20e6, key ="p", width = 200)
if st.button("Рассчитать"):
    try:
        t = get_si_value(t_v, t_u, "temperature")
        p = get_si_value(p_v, p_u, "pressure")
        dens, z = calc_dryair_dens(t, p)
        data ={"Температура сухого воздуха, °С": t, "Абсолютное давление, Па": p, "Коэффициент сжимаемости": z, "Плотность, кг/м3": dens}
        #result = f"Плотность {dens} кг/м<sup>3</sup> \n\n Коэффициент сжимаемости {z}".replace(".", ",")
        #st.markdown(result, unsafe_allow_html=True)
        print_result(data)

    except Exception as e:
        #st.markdown(f":orange-badge[⚠️ {str(e)}]")
        st.error(f"{str(e)}", icon="⚠️")

with st.expander("Дополнительно"):
    st.markdown("[Статья](https://dzen.ru/a/XzUUMppesQVXBAwF) Модуль для расчёта плотности сухого воздуха")
    st.markdown("[Таблица](https://medsv.github.io/dzen/0001/Плотность_сухого_воздуха.html) Зависимость плотности сухого воздуха от его температуры " \
    "при различных значениях абсолютного давления")

#show_footer()