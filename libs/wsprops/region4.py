"""
В модуле размещён класс Region4, содержащий методы для расчёта теплофизических свойств влажного пара (область 4)
Методика расчёта взята из документа
http://www.iapws.org/relguide/IF97-Rev.pdf
-------------------------------------------------
'Инженерные расчёты на Python'
https://zen.yandex.ru/id/5f33dcd5554adc5b33aaee83
https://medsv.github.io/dzen/
"""

__author__ = "Сергей Медведев"
__copyright__ = "Сергей Медведев, 2021"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Сергей Медведев"
__email__ = "medsv@yandex.ru"
__status__ = "Production"

from .paramsin import ParamsIn
from .region1 import Region1
from .region2 import Region2


class Region4(ParamsIn):
    """
    Класс содержит методы для расчёта теплофизических свойств влажного пара (область 4)
    """
    def __init__(self):
        """
        Инициализация параметров
        """
        ParamsIn.__init__(self)
        self.region1 = Region1()
        self.region2 = Region2()
        self.T_min = self.sc.T_min  # Минимальное значение температуры, K
        self.T_max = self.region1.T_max  # Максимальное значение температуры, K
        self.p_min = self.sc.p_min  # Минимальное значение давления, Па
        self.p_max = self.region1.p_sc_marg  # Максимальное значение давления, Па
        self.props_w = None  # Свойства влажного пара при степени сухости x = 0 (кипящая вода)
        self.props_s = None  # Свойства влажного пара при степени сухости x = 1 (сухой насыщенный пар)

    def props_px(self, p, x):
        """
        Расчёт теплофизических свойств влажного пара по давлению и степени сухости
        p: давление, Па
        x: степень сухости влажного пара x=[0; 1]
        return: словарь с вычисленными значениями теплофизических свойств
        """
        self.__calc_edges_points(p)
        self.__props_x(x)
        return self.props.copy()

    def __props_x(self, x):
        """
        Расчёт теплофизических свойств влажного пара степенью сухости x 
        x: степень сухости влажного пара x=[0; 1]
        return: None
        """
        for key in self.props_w:
            self.props[key] = self.props_w[key] * (1 - x) + self.props_s[key] * x
        self.props['p'] = self.props_w['p']
        self.props['T'] = self.props_w['T']
        self.props['x'] = x

    def props_ph(self, p, h):
        """
        Расчёт теплофизических свойств влажного пара по давлению и энтальпии
        p: давление, Па
        h: энтальпия, Дж/кг
        return: словарь с вычисленными значениями теплофизических свойств
        """    
        return self.__props_pX(p, h, 'h')
        
    def props_ps(self, p, s):
        """
        Расчёт теплофизических свойств влажного пара по давлению и энтропии
        p: давление, Па
        s: энтропия, Дж/кг/К
        return: словарь с вычисленными значениями теплофизических свойств
        """        
        return self.__props_pX(p, s, 's')

    def props_p(self, p):
        """
        Расчёт теплофизических свойств кипящей воды и сухого насыщенного пара при давлении p
        p: давление, Па
        return: кортеж двух словарей: 0 - кипящая вода, 1 - сухой насыщенный пар
        """
        self.__calc_edges_points(p)
        return self.props_w.copy(), self.props_s.copy()

    def __props_pX(self, p, value, X):
        """
        Расчёт теплофизических свойств влажного пара по давлению и h или s
        p: давление, Па
        X: 'h' или 's'
        return: словарь с вычисленными значениями теплофизических свойств
        """     
        self.__calc_edges_points(p)
        x = (value - self.props_w[X]) / (self.props_s[X] - self.props_w[X])
        self.__props_x(x)
        self.props[X] = value
        return self.props.copy()

    def _get_T_edges(self, p):
        """
        Определение граничных значений температуры в области при давлении p
        p: давление, Па
        return: кортеж (T_lower, T_upper) - нижнее и верхнее значения температуры, К
        """        
        T = self.sc.T_p(p)
        return T, T

    def __calc_edges_points(self, p):
        """
        Расчёт параметров на левой и правой границах области влажного пара для заданного p
        p: давление, Па
        return: None
        """
        T = self.sc.T_p(p)
        self.props_w = self.region1.props_Tp(T, p)
        self.props_s = self.region2.props_Tp(T, p)

    def Tp_in(self, T, p):
        """
        T и p являются взаимозависимыми параметрами для Области 4.
        Реализован с целью совместимости интерфейса с интерфейсом Области 1, 2
        return: False
        """
        return False

    def tp_in(self, t, p):
        """
        t и p являются взаимозависимыми параметрами для Области 4.
        Реализован с целью совместимости интерфейса с интерфейсом Области 1, 2
        return: False
        """
        return False

    def _pX_in(self, p, value, X):
        """
        Проверка нахождения пары параметров p, h или p, s в пределах области
        p: давление, Па
        value: значение второго параметра (h, Дж/кг или s, Дж/кг/К)
        X: 'h' или 's'
        return: True если точка находится внутри области, False в противном случае
        """
        if not self.p_in(p):
            return False
        self.__calc_edges_points(p)
        value_lower = self.props_w[X]
        value_upper = self.props_s[X]
        return value_lower <= value <= value_upper

    def px_in(self, p, x):
        """
        Проверка нахождения пары параметров p, x в пределах области
        p: давление, Па
        x: степень сухости x = [0; 1]
        return: True если точка находится внутри области, False в противном случае
        """
        return self.p_in(p) and self.x_in(x)

    def x_in(self, x):
        """
        Проверка корректности значения степени сухости
        x: степень сухости x = [0; 1]
        return: True если значение корректное, False в противном случае        
        """
        return 0. <= x <= 1.

    def dh_p(self, p):
        """
        Расчёт скрытой теплоты парообразования (h'' - h')
        p: давление, Па
        return: скрытая теплота парообразования, Дж/кг
        """
        self.__calc_edges_points(p)
        return  self.props_s['h'] - self.props_w['h']

    def ds_p(self, p):
        """
        Расчёт значения s'' - s'
        p: давление, Па
        return: значение s'' - s', Дж/кг/К
        """        
        self.__calc_edges_points(p)
        return  self.props_s['s'] - self.props_w['s']
