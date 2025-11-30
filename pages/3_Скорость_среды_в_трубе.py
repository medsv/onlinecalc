import streamlit as st
from math import pi
from common.print_result import print_result
from common.streamlit_components import create_unit_input, get_si_value, is_mass_flow

st.set_page_config(
    page_title="Расчёт скорости среды в трубе"
)


st.title("Расчёт скорости среды в трубе")
# d: float = st.number_input("Внутр. диаметр трубы, мм", value=85., step=1., min_value=6., max_value=5000., key ="d", width = 178)
d_v, d_u = create_unit_input(
        label="Внутр. диаметр трубы",
        category="length",
        key="d",
        value=85.0,
        step=1.,
        unit="мм"
        )
d: float = get_si_value(d_v, d_u, "length")

Q_v, Q_u = create_unit_input(
        label="Расход среды",
        category="flow",
        key="Q",
        value=50.0,
        step=1.,
        unit="м³/ч"
        )
Q = get_si_value(Q_v, Q_u, "flow")
if is_mass_flow(Q_u):
    dens_v, dens_u = create_unit_input(
        label="Плотность среды",
        category="density",
        key="dens",
        value=1000.0,
        step=1.,
        unit="кг/м3"
        )
    dens = get_si_value(dens_v, dens_u, "density")
    Q = Q / dens

if st.button("Рассчитать"):
    F: float = pi * d * d / 4  # площадь сечения трубы, м2 
    v: float = Q / F  # скорость среды
    data = {"Внутренний диаметр трубы, м": d, "Площадь сечения, м2": F, "Объёмный расход среды, м3/с": Q, "Скорость среды в трубе, м/с": v}
    print_result(data)