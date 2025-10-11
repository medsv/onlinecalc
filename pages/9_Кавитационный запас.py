import streamlit as st
from libs.wsprops import HSDiag
from common.footer import show_footer
from common.print_result import print_result

st.set_page_config(
    page_title="Расчёт кавитационного запаса",
    page_icon="💻",
    layout="centered"
)

st.title("Расчёт кавитационного запаса")
st.markdown("Рабочая жидкость - вода.")
with st.expander("Схема"):
    st.image("img/Кавитационный_запас_Схема.png")
    st.markdown("p - абсолютное давление над поверхностью воды, Па;\n\nt - температура воды, °С;\n\n" \
    "H - подпор, разница отметок поверхности воды и оси вала насоса (может принимать отрицательное значение), м;\n\n" \
        "dH - потери давления (напора) в подводящем трубопроводе, м.")

p: float = st.number_input("Давление, Па", value=101325.0, step=1., min_value=0., max_value=20e6, key ="p", width = 200)
t: float = st.number_input("Температура, °С", value=20., step=1., min_value=0., max_value= 623.15-273.15, key ="t", width = 200)
H: float = st.number_input("Подпор, м", value=0., step=1., min_value=-1000., max_value=1000., key ="H", width = 200)
dH: float = st.number_input("Потери давления (напора), м", value=0., step=1., min_value=0., max_value=1000., key ="dH", width = 200)
hs = HSDiag()
if st.button("Рассчитать"):
    try:
        props = hs.props_tp(t,p)
        if props["x"] > 0:
            st.error("Это пар", icon="⚠️")    
        else:
            ps: float = hs.sc.p_t(t)
            NPSH: float = H + (p - ps) * props["v"] / 9.81 - dH
            #data={"Кавитационный запас (NPSH), м": NPSH}
            data = {"Давление над поверхностью воды, Па": p, "Температура воды, °С": t, "Подпор, м": H, 
                    "Потери давления (напора), м": dH, "Кавитационный запас (NPSH), м": NPSH}
            print_result(data)

    except Exception as e:
        st.error(f"{str(e)}", icon="⚠️")

with st.expander("Дополнительно"):
    st.markdown("[Статья](https://dzen.ru/a/X8Nt8mPVdAQVSm6Z) Расчёт кавитационного запаса")
    st.markdown("[Статья](https://dzen.ru/a/YuQlMIkoykP0rEHz) Способ быстрой оценки кавитационного запаса насоса")
show_footer()