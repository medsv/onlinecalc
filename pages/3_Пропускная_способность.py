import streamlit as st
#from math import pi
from common.print_result import print_result
from common.streamlit_components import create_unit_input, get_si_value, is_mass_flow
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
    value=100000.,
    step=1.,
    unit="Па"
    )
dp: float = get_si_value(dp_v, dp_u, "pressure")

Q_v, Q_u = create_unit_input(
        label="Пропускная способность",
        category="volume_flow",
        key="Q",
        value=50.0,
        step=1.,
        unit="м³/ч"
        )

if st.button("Рассчитать"):
    pass