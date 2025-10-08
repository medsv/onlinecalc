"""
В модуле размещён родительский класс Region однофазных областей 1, 2
-------------------------------------------------
'Инженерные расчёты на Python'
https://zen.yandex.ru/id/5f33dcd5554adc5b33aaee83
https://medsv.github.io/dzen/
"""

__author__ = "Sergey Medvedev"
__copyright__ = "Sergey Medvedev, 2020"
__license__ = "GPL"
__version__ = "1.2"
__maintainer__ = "Sergey Medvedev"
__email__ = "medsv@yandex.ru"
__status__ = "Production"

from .paramsin import ParamsIn


class Region(ParamsIn):
    """
    Родительский класс для классов однофазных областей 1, 2.
    Содержит общие для области 1 и 2 методы
    """

    R = 461.526  # Газовая постоянная водяного пара, Дж/кг/К
    Tc = 647.096  # Температура в критической точке, К
    pc = 22.064e6  # Давление в критической точке, Па
    rc = 322  # Плотность в критической точке, кг/м3

    def __init__(self):
        ParamsIn.__init__(self)
        # Верхнее значение температуры после которого линия насыщения перестаёт быть границей между областями 1 и 2
        self.T_sc_marg = 623.15
        # Верхнее значение давления после которого линия насыщения перестаёт быть границей между областями 1 и 2
        self.p_sc_marg = self.sc.p_T(self.T_sc_marg)

    def props_Tp(self, T, p):
        """
        Расчёт теплофизических свойств воды и водяного пара по температуре и давлению.
        T: температура, К
        p: давление, Па
        return: словарь свойств
        """
        self._props_Tp(T, p)
        self.props['T'] = T
        self.props['p'] = p
        return self.props.copy()

    def props_tp(self, t, p):
        """
        Расчёт теплофизических свойств воды и водяного пара по температуре и давлению.
        t: температура, С
        p: давление, Па
        return: словарь свойств.
        """
        return self.props_Tp(t + 273.15, p)

    def props_ph(self, p, h):
        """
        Расчёт теплофизических свойств воды и водяного пара по давлению и энтальпии.
        p: давление, Па
        h: энтальпия, Дж/кг
        return: словарь свойств.
        """
        T = self.T_ph(p, h)
        self._props_Tp(T, p)
        self.props['T'] = T
        self.props['h'] = h
        return self.props.copy()

    def props_ps(self, p, s):
        """
        Расчёт теплофизических свойств воды и водяного пара по давлению и энтропии.
        p: давление, Па
        s: энтропия, Дж/кг/К
        return: словарь свойств.
        """
        T = self.T_ps(p, s)
        self._props_Tp(T, p)
        self.props['T'] = T
        self.props['s'] = s
        return self.props.copy()

    def _pX_in(self, p, value, X):
        """
        Проверка нахождения пары параметров [p, h] или [p, s] в пределах области
        p: давление, Па
        value: значение второго параметра (h, Дж/кг или s, Дж/кг/К)
        X: 'h' или 's'
        return: True если точка находится внутри области, False в противном случае
        """
        if not self.p_in(p):
            return False
        T_lower, T_upper = self._get_T_edges(p)
        value_lower = self.props_Tp(T_lower, p)[X]
        value_upper = self.props_Tp(T_upper, p)[X]
        return value_lower <= value <= value_upper

    def _props_Tp(self, T, p):
        """
        Абстрактный метод.
        Расчёт теплофизических свойств воды и водяного пара по температуре и давлению.
        T: температура, К
        p: давление, Па
        return: None
        """
        raise NotImplementedError("Метод должен быть переопределён")

    def T_ph(self, p, h):
        """
        Абстрактный метод.
        Определение температуры по давлению и энтальпии
        p: давление, Па
        h: энтальпия, Дж/кг
        return: температура, К
        """
        raise NotImplementedError('Метод должен быть переопределён')

    def T_ps(self, p, s):
        """
        Абстрактный метод.
        Определение температуры по давлению и энтропии
        p: давление, Па
        s: энтропии, Дж/кг/К
        return: температура, К
        """
        raise NotImplementedError('Метод должен быть переопределён')
