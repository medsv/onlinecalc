# boiling_calculator.py
import streamlit as st
from libs.wsprops import Region4
#from common.units_manager import UnitManager
from common.streamlit_components import create_unit_input, get_si_value
from common.print_result import print_result
st.title("Расчёт свойств влажного пара")
input_type = st.radio(
    "Выберите способ расчёта:",
    ["По давлению", "По температуре"],
    horizontal=True
)
r4 = Region4()
if input_type == "По давлению":
    st.markdown(f"Допустимые значения входных параметров: p = [{r4.p_min}; {r4.p_max}] Па".replace(".", ","))
    value, unit = create_unit_input(
        "Абсолютное давление",
        "pressure",
        "p",
        5000.,
        1.,
        "Па"
        )
else: # По температуре
    st.markdown(f"Допустимые значения входных параметров: t = [{r4.T_min - 273.15}; {r4.T_max - 273.15}] °С".replace(".", ","))
    value, unit = create_unit_input(
        "Температура",
        "temperature",
        "t",
        30.,
        1.,
        "°C"
        )   
x_value, x_unit = create_unit_input(
    "Степень сухости",
    "percent",
    "x",
    50.,
    1.,
    "%"
    )
    
if st.button("Рассчитать"):
    try:
        x: float = get_si_value(x_value, x_unit, "percent")
        if x < 0. or x > 1.:
            raise ValueError("Допустимое значение степени сухости пара x=[0%; 100%] (x=[0; 1])")
        if input_type == "По давлению":
            p: float = get_si_value(value, unit, "pressure")
            t = r4.sc.t_p(p)
        else:
            t: float = get_si_value(value, unit, "temperature")
            p = r4.sc.p_t(t)
        props: dict[str, None | float] = r4.props_px(p, x)
        dh: float = r4.dh_p(p)  # удельная скрытая теплота парообразования
        if props['v']:
            dens: float = 1. / props['v']
        data = {"Температура пара, °С": t, "Давление пара, Па": p, "Степень сухости, доля": x, 
                "Плотность пара, кг/м3": dens, "Удельная энтальпия, Дж/кг": props['h'], 
                "Удельная скрытая теплота парообразования, Дж/кг": dh, 
                "Удельная энтропия, Дж/кг/К": props['s'], "Удельная теплоёмкость при постоянном давлении, Дж/кг/К": props['cp'],
                "Удельная теплоёмкость при постоянном объёме, Дж/кг/К": props['cv'], "Удельный объём пара, м3/кг": props['v'], 
                "Удельная внутренняя энергия, Дж/кг": props['u']}
        print_result(data)
    except Exception as e:
        st.error(f"{str(e)}", icon="⚠️")
    
with st.expander("Дополнительно"):
    st.markdown("[Статья](https://dzen.ru/a/YGoBbLIHhgN5wKyQ) Расчёт теплофизических свойств влажного пара")
    

