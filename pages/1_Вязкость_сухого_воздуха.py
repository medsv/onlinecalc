import streamlit as st
#from libs.calcdryairdens import calc_dryair_dens
from libs.calcdryairvisc import calc_dryair_visc
from common.print_result import print_result
from common.streamlit_components import create_unit_input, get_si_value

st.set_page_config(
    page_title="Расчёт вязкости сухого воздуха",
)
# Заголовок страницы
st.title("Расчёт вязкости сухого воздуха")
st.markdown("Допустимые значения входных параметров: t = [-100; 1000] °С,  p = [0,1; 20] МПа.")

#t: float = st.number_input("Температура, °С", value=20., step=1., min_value=-100., max_value=1000., key ="t", width = 200)
#p: float = st.number_input("Абсолютное давление, Па", value=101325.0, step=1., min_value=100000., max_value=20e6, key ="p", width = 200)

t_v, t_u = create_unit_input(
        "Температура",
        "temperature",
        "t",
        20.,
        1.,
        "°C"
        )

p_v, p_u = create_unit_input(
        "Абсолютное давление",
        "pressure",
        "p",
        101325.0,
        1.,
        "Па"
        )

if st.button("Рассчитать"):
    try:
        t: float = get_si_value(t_v, t_u, "temperature")
        p: float = get_si_value(p_v, p_u, "pressure")
        dvisc,  dens = calc_dryair_visc(t, p)
        data ={"Температура сухого воздуха, °С": t, "Давление, Па": p, "Плотность, кг/м3": dens, 
               "Динамическая вязкость, Па*с": dvisc, "Кинематическая вязкость, м2/с": dvisc / dens}
        #result = f"Плотность {dens} кг/м<sup>3</sup> \n\n Коэффициент сжимаемости {z}".replace(".", ",")
        #st.markdown(result, unsafe_allow_html=True)
        print_result(data)

    except Exception as e:
        #st.markdown(f":orange-badge[⚠️ {str(e)}]")
        st.error(f"{str(e)}", icon="⚠️")

with st.expander("Дополнительно"):
    st.markdown("[Статья](https://dzen.ru/a/XzQBnx_sVWuS702C) Вязкость сухого воздуха")
    st.markdown("[Таблица](https://medsv.github.io/dzen/0002/Динамическая_вязкость_сухого_воздуха.html) Зависимость динамической " \
    "вязкости сухого воздуха от его температуры при различных значениях абсолютного давления")
    st.markdown("[Таблица](https://medsv.github.io/dzen/0002/Кинематическая_вязкость_сухого_воздуха.html) Зависимость кинематической " \
    "вязкости сухого воздуха от его температуры при различных значениях абсолютного давления")
