import streamlit as st
#from math import pi
from common.print_result import print_result
from common.streamlit_components import create_unit_input, get_si_value, is_mass_flow

st.set_page_config(
    page_title="Пропускная способность"
)

st.title("Пропускная способность")

with st.expander("Теория"):
    st.markdown("[Статья](https://dzen.ru/a/XzvV9MLXtVfwVFUh) Что такое Kv и как его использовать")

dens_v, dens_u = create_unit_input(
    label="Плотность среды",
    category="density",
    key="dens",
    value=1000.0,
    step=1.,
    unit="кг/м3"
    )
dens: float = get_si_value(dens_v, dens_u, "density")
dp_v, dp_u = create_unit_input(
    label="Потери давления",
    category="pressure",
    key="p",
    value=0.1,
    step=1.,
    unit="МПа"
    )
dp: float = get_si_value(dp_v, dp_u, "pressure")

Kv_v, Kv_u = create_unit_input(
        label="Пропускная способность",
        category="volume_flow",
        key="Q",
        value=50.0,
        step=1.,
        unit="м³/ч"
        )
Kv: float = get_si_value(Kv_v, Kv_u, "volume_flow")  # м3/c
Kv *= 3600.  #м3/ч

if st.button("Рассчитать"):
    Q = Kv * (dp / 100 / dens) ** 0.5
    data = {"Пропускная способность, м3/ч": Kv, "Потери давления, Па": dp, 
            "Плотность среды, кг/м3": dens, "Расход среды, м3/ч": Q, "Расход среды, м3/c": Q / 3600.}
    print_result(data)