import streamlit as st
from libs.wetairprops import calc_d, calc_t_wb, calc_t_dp_d, calc_dens, calc_p_s, calc_I, calc_RH_d, t_min, t_max, p_min, p_max
from common.footer import show_footer
from common.print_result import print_result
from common.streamlit_components import create_unit_input, get_si_value


st.set_page_config(
    page_title="Расчёт параметров влажного воздуха",
)

# Заголовок страницы
st.title("Расчёт параметров влажного воздуха")
st.markdown(f"Допустимые значения входных параметров: t= [-100; +200] °С.")

input_type = st.radio(
    "Выберите способ расчёта:",
    ["По относительной влажности", "По влагосодержанию"],
    horizontal=True
)

t_v, t_u = create_unit_input(
    label="Температура",
    category="temperature",
    key="t",
    value=20.,
    step=1.,
    unit="°C"
    )

if input_type == "По относительной влажности":
    RH_v, RH_u = create_unit_input(
        label="Относительная влажность",
        category="percent",
        key="RH",
        value=60.,
        step=1.,
        unit="%"
        )
else:
    d_v, d_u = create_unit_input(
        label="Влагосодержание",
        category="mass_content",
        key="d",
        value=8.7168,
        form="%.4f",
        step=0.0001,
        unit="г/кг"
        )

p_v, p_u = create_unit_input(
    label="Абсолютное давление",
    category="pressure",
    key="p",
    value=101325.,
    step=1.,
    unit="Па"
    )



def calc(t: float, RH_d : float, p: float, RH_d_sel: str):
    if p <= 0:
        raise ValueError('Значение давления p должно быть больше нуля.')
    if RH_d_sel == 'RH, %':
        # RH в долях единицы, а не в процентах
        #RH = RH_d / 100.
        RH = RH_d
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










s = """
    t - температура влажного воздуха, °С;\n
    RH - относительная влажность, доли;\n
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
    # Получаем значения в СИ
    t = get_si_value(t_v, t_u, "temperature")
    p = get_si_value(p_v, p_u, "pressure")
    if input_type == "По относительной влажности":
        RH = get_si_value(RH_v, RH_u, "percent")
        # Преобразуем RH из процентов в доли
        RH_d = RH
        RH_d_sel = "RH, %"
    else:
        d = get_si_value(d_v, d_u, "mass_content")
        RH_d = d
        RH_d_sel = "d, г/кг с.в."
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