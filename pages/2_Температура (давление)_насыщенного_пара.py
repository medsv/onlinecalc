# boiling_calculator.py
import streamlit as st
from libs.wetairprops import calc_p_s, calc_t_s, p_min, p_max, t_min, t_max
#from common.units_manager import UnitManager
from common.streamlit_components import create_unit_input, get_si_value
from common.print_result import print_result
st.title("Определение температуры / давления насыщенного водяного пара")
input_type = st.radio(
    "Выберите способ расчёта:",
    ["По давлению", "По температуре"],
    horizontal=True
)
if input_type == "По давлению":
    st.markdown(f"Допустимые значения входных параметров: p = [{p_min}; {p_max}] Па".replace(".", ","))
    value, unit = create_unit_input(
        "Давление",
        "pressure",
        "p",
        101325.,
        1.,
        "Па"
        )
else: # По температуре
    st.markdown(f"Допустимые значения входных параметров: t = [{t_min}; {t_max}] °С".replace(".", ","))
    value, unit = create_unit_input(
        "Температура",
        "temperature",
        "t",
        20.,
        1.,
        "°C"
        )    
if st.button("Рассчитать"):
    try:
        if input_type == "По давлению":
            p: float = get_si_value(value, unit, "pressure")
            t: float = calc_t_s(p)
        else:
            t: float = get_si_value(value, unit, "temperature")
            p: float = calc_p_s(t)    
        data = {"Давление насыщенного водяного пара, Па": p, "Температура насыщения (точки росы), °С": t}
        print_result(data)
    except Exception as e:
        st.error(f"{str(e)}", icon="⚠️")
    

