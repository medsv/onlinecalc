import streamlit as st
from libs.wetairprops import calc_d, calc_t_wb, calc_t_dp_d, calc_dens, calc_p_s, calc_I, calc_RH_d
from common.footer import show_footer
from common.print_result import print_result

st.set_page_config(
    page_title="Расчёт параметров влажного воздуха",
    page_icon="💻",
    layout="centered"
)

# Инициализация состояния сессии для хранения текущих значений и параметров
if 'rh_d_sel' not in st.session_state:
    st.session_state.rh_d_sel = "RH, %"
if 'rh_d_value' not in st.session_state:
    st.session_state.rh_d_value = 60.0
if 'rh_d_min' not in st.session_state:
    st.session_state.rh_d_min = 0.0
if 'rh_d_max' not in st.session_state:
    st.session_state.rh_d_max = 100.0  # Для RH в процентах
if 'rh_d_format' not in st.session_state:
    st.session_state.rh_d_format = "%0.1f"
if 'rh_d_step' not in st.session_state:
    st.session_state.rh_d_step = 1.

def calc(t: float, RH_d : float, p: float, RH_d_sel: str):
    if p <= 0:
        raise ValueError('Значение давления p должно быть больше нуля.')
    if RH_d_sel == 'RH, %':
        # RH в долях единицы, а не в процентах
        RH = RH_d / 100.
        if not (0.<=RH<=1.):
            raise ValueError('Значение относительной влажности RH должно находиться в диапазоне (0%; 100%].')
        d: float = calc_d(t, RH, p)
    else:  # d
        if RH_d < 0:
            raise ValueError('Значение влагосодержания d должно быть больше нуля.')
        RH: float = calc_RH_d(t, RH_d, p)
        d = RH_d

    p_s: float = calc_p_s(t) 
    p_st: float = p_s * RH
    
    

    d1: float = d / (1 + d / 1000.)  # на кг влажного воздуха
    I: float = calc_I(t, RH, p)
    I1: float = I / (1 + d / 1000.)  # на кг влажного воздуха
    t_wb: float = calc_t_wb(t, RH, p)
    t_dp: float = calc_t_dp_d(d, p)


    dens: float = calc_dens(t, RH, p)
    p_cond: float = p / RH
    RH *= 100
    return {"t": t, "RH": RH, "p": p, "d": d, "d1": d1, "dens": dens, "t_wb": t_wb, "t_dp": t_dp, "I": I, "I1": I1, "p_s": p_s, "p_st": p_st, "p_cond": p_cond}


def update_rh_d_params():
    if st.session_state.RH_d_sel == "RH, %":
        st.session_state.rh_d_min = 0.0
        st.session_state.rh_d_max = 100.0
        st.session_state.rh_d_value = 60.
        st.session_state.rh_d_format = "%0.1f"
        st.session_state.rh_d_step = 1.
    else:  # "d, г/кг с.в."
        st.session_state.rh_d_min = 0.0
        st.session_state.rh_d_max = 1000.0
        st.session_state.rh_d_value = 8.716840927527572
        st.session_state.rh_d_format = "%0.4f"
        st.session_state.rh_d_step = .01

WIDTH: int = 310
COLS_SIZE = [4, 5]
# Заголовок страницы
st.title("Расчёт параметров влажного воздуха")
st.markdown("Диапазон допустимых температур от -100 °С до +200 °С.")

# Создаем контейнер с колонками
col1, col2  = st.columns(COLS_SIZE, vertical_alignment="center", width = WIDTH)
with col1:  
    st.write("t, °С")
with col2:
    t = st.number_input("Температура", value=20., step=1., min_value=-100., max_value=200., key ="t", label_visibility="collapsed")

col1, col2  = st.columns(COLS_SIZE, vertical_alignment="center", width = WIDTH)
with col1:  
    RH_d_sel = st.selectbox(
        "Параметр влажности",
        options=["RH, %", "d, г/кг с.в."],
        label_visibility="collapsed",
        width=150,
        key="RH_d_sel",
        on_change=update_rh_d_params
        )
with col2:
    RH_d = st.number_input(
        "Значение параметра влажности",
        label_visibility="collapsed",
        value=st.session_state.get("rh_d_value"),
        min_value=st.session_state.get("rh_d_min"),
        max_value=st.session_state.get("rh_d_max"),
        format = st.session_state.get("rh_d_format"),
        step=st.session_state.get("rh_d_step"),
        key="RH_d"
        )

col1, col2  = st.columns(COLS_SIZE, vertical_alignment="center", width = WIDTH)
with col1:  
    st.write("p, Па")
with col2:
    p = st.number_input("Давление", value=101325.0, step=1., key ="p", label_visibility="collapsed")

s = """
    t - температура влажного воздуха, °С;\n
    RH - относительная влажность, %;\n
    p - абсолютное давление влажного воздуха, Па;\n 
    d - влагосодержание, г на кг сухого воздуха;\n 
    d1 - влагосодержание, г на кг влажного воздуха;\n
    dens - плотность влажного воздуха, кг/м3;\n
    t_wb - температура мокрого термометра, °С;\n
    t_dp - температура точки росы, °С;\n
    I - энтальпия влажного воздуха, кДж/(кг сухого воздуха);\n
    I1 - энтальпия влажного воздуха, кДж/(кг влажного воздуха);\n
    p_s - давление насыщения (упругость водяного пара), Па;\n
    p_st - парциальное давление пара, Па;\n
    p_cond - давление начала образования конденсата, Па
    """


if st.button("Рассчитать"):
    try:
        result = calc(t, RH_d, p, RH_d_sel)

        # Создаем маппинг ключей
        key_mapping = {}
        for line in s.strip().split(';\n'):
            if '-' in line:
                old_key, description = line.split('-', 1)
                old_key = old_key.strip()
                description = description.strip().rstrip(';')
                key_mapping[old_key] = description[0].upper() + description[1:]

        # Создаем новый словарь
        data = {key_mapping.get(old_key, old_key): value for old_key, value in result.items()}      
        print_result(data)

    except Exception as e:
        #st.markdown(f":orange-badge[⚠️ {str(e)}]")
        st.error(f"{str(e)}", icon="⚠️")
with st.expander("Дополнительно"):
    st.markdown("[Статья](https://dzen.ru/a/Yt0vpHeCWWlWEfPq) Модуль для расчёта свойств влажного воздуха")
#show_footer()