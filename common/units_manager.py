# units_manager.py
class UnitManager:
    """Централизованный менеджер единиц измерения для Streamlit приложения"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_units()
        return cls._instance
    
    def _initialize_units(self):
        """Инициализация всех единиц измерения"""
        # Базовые определения
        self._base_units = {
            "pressure": {
                "Па": lambda x: x,
                "кПа": lambda x: x * 1000,
                "МПа": lambda x: x * 1e6,
                "бар": lambda x: x * 1e5,
                "атм": lambda x: x * 101325,
                "мм.рт.ст.": lambda x: x * 133.322,
            },
            "temperature": {
                "°C": lambda x: x,
                "K": lambda x: x + 273.15,
                "°F": lambda x: (x - 32) * 5/9,
            },
            "volume_flow": {
                "м³/с": lambda x: x,
                "л/с": lambda x: x * 0.001,
                "м³/ч": lambda x: x / 3600,
                "л/мин": lambda x: x * 0.001 / 60,
                "л/ч": lambda x: x * 0.001 / 3600,
            },
            "mass_flow": {
                "кг/с": lambda x: x,
                "кг/ч": lambda x: x / 3600,
                "т/ч": lambda x: x * 1000 / 3600,
            },
            "density": {
                "кг/м³": lambda x: x,
                "г/см³": lambda x: x * 1000,
                "т/м³": lambda x: x * 1000,
            },
            "length": {
                "м": lambda x: x,
                "см": lambda x: x * 0.01,
                "мм": lambda x: x * 0.001,
                "км": lambda x: x * 1000,
            },
            "enthalpy": {
                "кДж/кг": lambda x: x * 1000,
                "Дж/кг": lambda x: x,
                "ккал/кг": lambda x: x * 4186.8,
            }
        }
        
        # Создаем объединенную категорию flow
        self._base_units["flow"] = {**self._base_units["volume_flow"], **self._base_units["mass_flow"]}
        
        # Кэш для быстрого доступа
        self._units_cache = {category: list(units.keys()) for category, units in self._base_units.items()}
        self._mass_flow_units = set(self._base_units["mass_flow"].keys())
    
    def get_units(self, category: str) -> list:
        """Получить список единиц измерения для категории"""
        return self._units_cache.get(category, [])
    
    def to_si(self, value: float, unit: str, category: str) -> float:
        """Преобразовать значение в СИ"""
        if category in self._base_units and unit in self._base_units[category]:
            return self._base_units[category][unit](value)
        raise ValueError(f"Неизвестная единица '{unit}' для категории '{category}'")
    
    def is_mass_flow(self, unit: str) -> bool:
        """Проверить, является ли единица измерения массовым расходом"""
        return unit in self._mass_flow_units