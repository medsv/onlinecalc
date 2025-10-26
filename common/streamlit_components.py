# streamlit_components.py
import streamlit as st
from .units_manager import UnitManager

# Создаем единственный экземпляр менеджера
_unit_manager = UnitManager()

def create_unit_input(
    label: str, 
    category: str, 
    key: str, 
    value: float = 0.0,
    step: float = 1.,
    unit: str = None,
) -> tuple[float, str]:
    """
    Создает унифицированный элемент ввода с выбором единиц измерения
    """
    available_units = _unit_manager.get_units(category)
    
    if not available_units:
        st.error(f"Нет доступных единиц для категории '{category}'")
        return value, ""
    
    # Определяем единицу по умолчанию
    if unit not in available_units:
        unit = available_units[0]
    
    # Создаем элементы ввода
    WIDTH: int = 310
    COLS_SIZE = [3, 2]
    col1, col2  = st.columns(COLS_SIZE, vertical_alignment="center", width = WIDTH)
    
    with col1:
        value = st.number_input(
            label=label,
            value=value,
            key=f"{key}_value",
            step = step,
            width = 200
        )
    
    with col2:
        unit = st.selectbox(
            label="",
            options=available_units,
            index=available_units.index(unit),
            key=f"{key}_unit",
            width = 150
            #label_visibility="collapsed"
        )
    
    return value, unit

def get_si_value(value: float, unit: str, category: str) -> float:
    """
    Получить значение в СИ
    """
    return _unit_manager.to_si(value, unit, category)

def is_mass_flow(unit: str) -> bool:
    """
    Проверить, является ли единица измерения массовым расходом
    """
    return _unit_manager.is_mass_flow(unit)