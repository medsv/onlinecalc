import streamlit as st
from common.print_result import print_result
from libs.wsprops.region1 import Region1
from libs.calcwsdvisc import calc_ws_dvisc
from common.streamlit_components import create_unit_input, get_si_value

st.set_page_config(
    page_title="Расчёт свойств воды",
)
st.title("Расчёт свойств воды")
st.markdown("Допустимые значения входных параметров: t = [0; 350] °С,  p = [611,213 Па; 100 МПа].")
with st.expander("Расчётная область - область 1"):
    st.image("img/Области_IAPWS-IF97.png")

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

water = Region1()
if st.button("Рассчитать"):
    try:
        t: float = get_si_value(t_v, t_u, "temperature")
        p: float = get_si_value(p_v, p_u, "pressure")
        if p > 100e6: raise Exception("Абсолютное давление должно быть не больше 100 МПа")
        if not water.Tp_in(t + 273.15, p):
            t_cor = water.sc.t_p(p)
            p_cor = water.sc.p_t(t)
            mes: str = f"Сочетание введённых значений температуры и давления соответствует пару. Для воды либо давление должно быть выше {p_cor} Па, либо температура должна быть ниже {t_cor} °С."
            st.error(mes, icon="⚠️")
        else:
        #try:
            ts: None | float = None; ps: None | float = None  # для того, чтобы в результате расчётов выводилось none
            props = water.props_tp(t, p)
            # Validate that props['v'] exists and is not zero before division
            v: None | float = props.get('v')
            if v is None or v == 0.:
                raise Exception("Не удалось вычислить удельный объем воды")
            dens: float = 1. / v
            if 0 <= t <= 647.096 - 273.15:
                ps = water.sc.p_t(t)
            if 611.212677 <= p <= 22.064e6:
                ts = water.sc.t_p(p)
            dvisc: float = calc_ws_dvisc(t, dens)
            kvisc: float = dvisc / dens
            data = {"Температура воды, °С": t, "Давление воды, Па": p, "Плотность воды, кг/м3": dens, 
                    "Кинематическая вязкость, м2/с": kvisc, "Динамическая вязкость, Па*с": dvisc, "Удельная энтальпия, Дж/кг": props['h'], 
                    "Удельная энтропия, Дж/кг/К": props['s'], "Удельная теплоёмкость при постоянном давлении, Дж/кг/К": props['cp'],
                    "Удельная теплоёмкость при постоянном объёме, Дж/кг/К": props['cv'], "Удельный объём воды, м3/кг": props['v'], 
                    "Удельная внутренняя энергия, Дж/кг": props['u'], "Скорость звука, м/с": props['w'], "Давление кипения воды, Па": ps, 
                    "Температура кипения воды, °С": ts}
            print_result(data)

    except Exception as e:
        st.error(f"{str(e)}", icon="⚠️")

with st.expander("Дополнительно"):
    st.markdown("[Статья](https://dzen.ru/a/X0qh9a5aWlqL4uAF) Расчёт теплофизических свойств воды")
    st.markdown("[Статья](https://dzen.ru/a/XzeDP4NiCA2EbFYa) Вязкость воды и водяного пара + Табличные данные")
