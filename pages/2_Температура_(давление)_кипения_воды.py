# boiling_calculator.py
import streamlit as st
from libs.wsprops import SaturationCurve as SC
#from common.units_manager import UnitManager
from common.streamlit_components import create_unit_input, get_si_value
from common.print_result import print_result
st.title("Определение температуры / давления кипения воды")
sc = SC()
input_type = st.radio(
    "Выберите способ расчёта:",
    ["По давлению", "По температуре"],
    horizontal=True
)
if input_type == "По давлению":
    st.markdown(f"Допустимые значения входных параметров: p = [{sc.p_min}; {sc.p_max}] Па".replace(".", ","))
    value, unit = create_unit_input(
        "Давление",
        "pressure",
        "p",
        101325.,
        1.,
        "Па"
        )
else: # По температуре
    st.markdown(f"Допустимые значения входных параметров: t = [{sc.T_min - 273.15}; {sc.T_max - 273.15}] °С".replace(".", ","))
    value, unit = create_unit_input(
        "Температура",
        "temperature",
        "t",
        100.,
        1.,
        "°C"
        )    
if st.button("Рассчитать"):
    try:
        if input_type == "По давлению":
            p: float = get_si_value(value, unit, "pressure")
            t: float = sc.t_p(p)
        else:
            t: float = get_si_value(value, unit, "temperature")
            p: float = sc.p_t(t)    
        data = {"Температура кипения воды, °С": t, "Давление кипения воды, Па": p}
        print_result(data)
    except Exception as e:
        st.error(f"{str(e)}", icon="⚠️")
    

