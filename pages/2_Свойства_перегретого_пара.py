import streamlit as st
from common.print_result import print_result
from libs.wsprops.region2 import Region2
from libs.calcwsdvisc import calc_ws_dvisc 
st.set_page_config(
    page_title="Расчёт свойств перегретого пара",
)
st.title("Расчёт свойств перегретого пара")
#st.markdown("Допускаемые значения величин: t = [0; 350] °С,  p = [611,213 Па; 100 МПа]")
t: float = st.number_input("Температура, °С", value=150., step=1., min_value=0., max_value= 800., key ="t", width = 200)
#p: float = st.number_input("Абсолютное давление, Па", value=23.5e6, step=1e3, min_value=0., max_value=100.e6, key ="p", width = 200)
WIDTH: int = 310
COLS_SIZE = [3, 2]
col1, col2  = st.columns(COLS_SIZE, vertical_alignment="center", width = WIDTH)
with col1:  
    p: float = st.number_input("Абсолютное давление", value=101325.0, step=1., min_value=0., key ="p", width = 200)
with col2:
    flow_dim: str = st.selectbox(
        " ",
        options=["Па", "кПа", "кгс/см2", "бар", "МПа"],
        width=150,
        key="p_dim",
        )
steam = Region2()
if st.button("Рассчитать"):
    k: float = 1.
    if flow_dim == "кПа": k = 1e3
    elif flow_dim == "кгс/см2": k = 98066.5
    elif flow_dim == "бар": k = 1e5
    elif flow_dim == "МПа": k = 1e6
    p *= k
    if not steam.Tp_in(t + 273.15, p):
        #t_cor = water.sc.t_p(p)
        #p_cor = water.sc.p_t(t)
        st.error("Сочетание введённых значений температуры и давления находится вне расчётной области.", icon="⚠️")
    else:
        try:
            ts = None; ps = None  # для того, чтобы в результате расчётов выводилось none
            props = steam.props_tp(t,p)
            dens: float = 1. / props['v']            
            if p <= 22.064e6:
                ts: float = steam.sc.t_p(p)
            if t <= 647.096 - 273.15:
                ps: float = steam.sc.p_t(t)
            dvisc: float = calc_ws_dvisc(t, dens)
            kvisc: float = dvisc / dens            
            data = {"Температура пара, °С": t, "Давление пара, Па": p, "Плотность пара, кг/м3": dens, 
                    "Кинематическая вязкость, м2/с": kvisc, "Динамическая вязкость, Па*с": dvisc, "Удельная энтальпия, Дж/кг": props['h'], 
                    "Удельная энтропия, Дж/кг/К": props['s'], "Удельная теплоёмкость при постоянном давлении, Дж/кг/К": props['cp'],
                    "Удельная теплоёмкость при постоянном объёме, Дж/кг/К": props['cv'], "Удельный объём пара, м3/кг": props['v'], 
                    "Удельная внутренняя энергия, Дж/кг": props['u'], "Скорость звука, м/с": props['w'], "Давление конденсации пара, Па": ps, 
                    "Температура конденсации пара, °С": ts}
            print_result(data)

        except Exception as e:
            st.error(f"{str(e)}", icon="⚠️")

with st.expander("Дополнительно"):
    st.markdown("[Статья](https://dzen.ru/a/X28KwGOyXQTNWPOL) Расчёт теплофизических свойств перегретого пара")
    st.markdown("[Статья](https://dzen.ru/a/XzeDP4NiCA2EbFYa) Вязкость воды и водяного пара + Табличные данные")
