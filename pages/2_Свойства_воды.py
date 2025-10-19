import streamlit as st
from common.print_result import print_result
from libs.wsprops.region1 import Region1
st.set_page_config(
    page_title="Расчёт свойств воды",
)
st.title("Расчёт свойств воды")
st.markdown("Допускаемые значения величин: t = [0; 350] °С,  p = [611,213 Па; 100 МПа]")
t: float = st.number_input("Температура, °С", value=20., step=1., min_value=0., max_value= 350., key ="t", width = 200)
p: float = st.number_input("Абсолютное давление, Па", value=101325.0, step=1., min_value=611.213, max_value=100e6, key ="p", width = 200)
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
            ts: float = water.sc.t_p(p)
            data = {"Температура воды, °С": t, "Давление воды, Па": p, "Плотность воды, кг/м3": 1. / props['v'], "Удельная энтальпия, Дж/кг": props['h'], 
                    "Удельная энтропия, Дж/кг/К": props['s'], "Удельная теплоёмкость при постоянном давлении, Дж/кг/К": props['cp'],
                    "Удельная теплоёмкость при постоянном объёме, Дж/кг/К": props['cv'], "Удельный объём воды, м3/кг": props['v'], 
                    "Удельная внутренняя энергия, Дж/кг": props['u'], "Скорость звука, м/с": props['w'], "Давление кипения воды, Па": ps, 
                    "Температура кипения воды, °С": ts}
            print_result(data)

        except Exception as e:
            st.error(f"{str(e)}", icon="⚠️")

with st.expander("Дополнительно"):
    st.markdown("[Статья](https://dzen.ru/a/X0qh9a5aWlqL4uAF) Расчёт теплофизических свойств воды")
