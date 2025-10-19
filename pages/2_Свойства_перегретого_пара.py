import streamlit as st
from common.print_result import print_result
from libs.wsprops.region2 import Region2
st.set_page_config(
    page_title="Расчёт свойств перегретого пара",
)
st.title("Расчёт свойств перегретого пара")
#st.markdown("Допускаемые значения величин: t = [0; 350] °С,  p = [611,213 Па; 100 МПа]")
t: float = st.number_input("Температура, °С", value=540., step=1., min_value=0., max_value= 800., key ="t", width = 200)
p: float = st.number_input("Абсолютное давление, Па", value=23.5e6, step=1e3, min_value=0., max_value=100.e6, key ="p", width = 200)
steam = Region2()
if st.button("Рассчитать"):
    if not steam.Tp_in(t + 273.15, p):
        #t_cor = water.sc.t_p(p)
        #p_cor = water.sc.p_t(t)
        mes = f"Сочетание введённых значений температуры и давления находится вне расчётной области."
        st.error(mes, icon="⚠️")
    else:
        try:
            props = steam.props_tp(t,p)
            ts= None; ps = None
            if p <= 22.064e6:
                ts: float = steam.sc.t_p(p)
            if t <= 647.096 - 273.15:
                ps: float = steam.sc.p_t(t)
            data = {"Температура пара, °С": t, "Давление пара, Па": p, "Плотность пара, кг/м3": 1. / props['v'], "Удельная энтальпия, Дж/кг": props['h'], 
                    "Удельная энтропия, Дж/кг/К": props['s'], "Удельная теплоёмкость при постоянном давлении, Дж/кг/К": props['cp'],
                    "Удельная теплоёмкость при постоянном объёме, Дж/кг/К": props['cv'], "Удельный объём пара, м3/кг": props['v'], 
                    "Удельная внутренняя энергия, Дж/кг": props['u'], "Скорость звука, м/с": props['w'], "Давление конденсации пара, Па": ps, 
                    "Температура конденсации пара, °С": ts}
            print_result(data)

        except Exception as e:
            st.error(f"{str(e)}", icon="⚠️")

with st.expander("Дополнительно"):
    st.markdown("[Статья](https://dzen.ru/a/X28KwGOyXQTNWPOL) Расчёт теплофизических свойств перегретого пара")
