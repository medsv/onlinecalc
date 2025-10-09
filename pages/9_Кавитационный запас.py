import streamlit as st
from libs.wsprops import HSDiag
from common.footer import show_footer

st.set_page_config(
    page_title="Расчёт кавитационного запаса",
    page_icon="💻",
    layout="centered"
)

st.title("Расчёт кавитационного запаса")
st.markdown("Рабочая жидкость - вода.")
with st.expander("Схема"):
    st.image("img/Кавитационный_запас_Схема.png")
    st.markdown("P - абсолютное давление над поверхностью воды, Па;\n\nt - температура воды, °С;\n\n" \
    "H - подпор, разница отметок поверхности воды и оси вала насоса (может иметь принимать значение), м;\n\n" \
        "dH - потери давления (напора) в подводящем трубопроводе, м.")

p: float = st.number_input("Давление P, Па", value=101325.0, step=1., min_value=0., max_value=20e6, key ="p", width = 200)
t: float = st.number_input("Температура t, °С", value=20., step=1., min_value=0., max_value=500., key ="t", width = 200)
H: float = st.number_input("Подпор H, м", value=0., step=1., min_value=-10., max_value=1000., key ="H", width = 200)
dH: float = st.number_input("Потери напора dH, м", value=0., step=1., min_value=0., max_value=1000., key ="dH", width = 200)
hs = HSDiag()
if st.button("Рассчитать"):
    try:
        props = hs.props_tp(t,p)
        if props["x"] > 0:
            st.error("Это пар", icon="⚠️")    
        else:
            ps = hs.sc.p_t(t)
            NPSH = H + (p - ps) * props["v"] / 9.81 - dH
            st.markdown(f"Кавитационный запас {round(NPSH, 1)} м".replace(".", ","))

    except Exception as e:
        st.error(f"{str(e)}", icon="⚠️")

with st.expander("Дополнительно"):
    st.markdown("[Статья](https://dzen.ru/a/X8Nt8mPVdAQVSm6Z) Расчёт кавитационного запаса")
    st.markdown("[Статья](https://dzen.ru/a/YuQlMIkoykP0rEHz) Способ быстрой оценки кавитационного запаса насоса")
show_footer()