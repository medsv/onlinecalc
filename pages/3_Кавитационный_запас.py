import streamlit as st
from libs.wsprops.region1 import Region1
from common.print_result import print_result

st.set_page_config(
    page_title="Расчёт кавитационного запаса",
)

st.title("Расчёт кавитационного запаса")
st.markdown("Допускаемые значения величин: t = [0; 350] °С,  p = [611,213 Па; 100 МПа]")
st.markdown("Рабочая жидкость - вода.")
with st.expander("Схема"):
    st.image("img/Кавитационный_запас_Схема.png")
    st.markdown("p - давление (абсолютное) над поверхностью воды, Па;\n\nt - температура воды, °С;\n\n" \
    "H - подпор, разница отметок поверхности воды и оси вала насоса (может принимать отрицательные значения), м;\n\n" \
        "dH - потери давления (напора) в подводящем трубопроводе, м.")

p: float = st.number_input("Абсолютное давление, Па", value=101325.0, step=1., min_value=611.213, max_value=100e6, key ="p", width = 200)
t: float = st.number_input("Температура, °С", value=20., step=1., min_value=0., max_value= 623.15-273.15, key ="t", width = 200)
H: float = st.number_input("Подпор, м", value=0., step=1., min_value=-1000., max_value=1000., key ="H", width = 200)
dH: float = st.number_input("Потери давления (напора), м", value=0., step=1., min_value=0., max_value=1000., key ="dH", width = 200)
water = Region1()
if st.button("Рассчитать"):
    if not water.Tp_in(t + 273.15, p):
        t_cor = water.sc.t_p(p)
        p_cor = water.sc.p_t(t)
        mes = f"Сочетание введённых значений температуры и давления соответствует пару. Для воды либо давление должно быть выше {p_cor} Па, либо температура должна быть ниже {t_cor} °С."
        st.error(mes, icon="⚠️")
    else:
        try:
            props = water.props_tp(t,p)
            ps: float = water.sc.p_t(t)
            NPSH: float = H + (p - ps) * props["v"] / 9.81 - dH
            #data={"Кавитационный запас (NPSH), м": NPSH}
            data = {"Давление над поверхностью воды, Па": p, "Температура воды, °С": t, "Подпор, м": H, 
                    "Потери давления (напора), м": dH, "Давление кипения воды, Па": ps, "Плотность воды, кг/м3": 1. / props['v'], "Кавитационный запас (NPSH), м": NPSH}
            print_result(data)

        except Exception as e:
            st.error(f"{str(e)}", icon="⚠️")

with st.expander("Дополнительно"):
    st.markdown("[Статья](https://dzen.ru/a/X8Nt8mPVdAQVSm6Z) Расчёт кавитационного запаса")
    st.markdown("[Статья](https://dzen.ru/a/YuQlMIkoykP0rEHz) Способ быстрой оценки кавитационного запаса насоса")
