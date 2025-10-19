import streamlit as st
from math import pi
from common.print_result import print_result

st.set_page_config(
    page_title="Расчёт скорости среды в трубе"
)


st.title("Расчёт скорости среды в трубе")
d: float = st.number_input("Внутр. диаметр трубы, мм", value=85., step=1., min_value=6., max_value=5000., key ="d", width = 175)

WIDTH: int = 310
COLS_SIZE = [3, 2]
col1, col2  = st.columns(COLS_SIZE, vertical_alignment="center", width = WIDTH)
with col1:  
    Q: float = st.number_input("Расход среды", value=50.0, step=1., min_value=0., max_value=10000., key ="Q", width = 200)
with col2:
    flow_dim: str = st.selectbox(
        " ",
        options=["м3/ч", "м3/с", "л/мин", "л/с", "т/ч", "кг/с"],
        #label_visibility="collapsed",
        width=150,
        key="flow_dim",
        #on_change=update_flow_dim
        )
if flow_dim == "т/ч" or flow_dim == "кг/с":
    dens: float = st.number_input("Плотность среды, кг/м3", value=1000., step=1., min_value=0.0001, max_value=5000., key ="dens", width = 175)
if st.button("Рассчитать"):
    if flow_dim == "м3/ч": k: float = 1. / 3600
    elif flow_dim == "м3/с": k: float = 1.
    elif flow_dim == "л/мин": k: float = 1. / 1000 / 60
    elif flow_dim == "л/с": k: float = 1. / 1000
    elif flow_dim == "т/ч": k: float = 1000. / dens / 3600
    elif flow_dim == "кг/с": k: float = 1. / dens
    Q *= k
    F: float = pi * d * d / 4 / 1e6  # площадь сечения трубы, м2 
    v: float = Q / F  # скорость среды
    data = {"Внутренний диаметр трубы, мм": d, "Площадь сечения, м2": F, "Объёмный расход среды, м3/с": Q, "Скорость среды в трубе, м/с": v}
    print_result(data)