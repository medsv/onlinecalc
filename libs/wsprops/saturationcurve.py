"""
Определение давления насыщения водяного пара по температуре и определение температуры насыщения по давлению.
Методика расчёта взята из документа
'Revised Release on the IAPWS Industrial Formulation 1997 for the Thermodynamic Properties of Water
and Steam (The revision only relates to the extension of region 5 to 50 MPa)'
Раздел '8 Equations for Region 4'
http://www.iapws.org/relguide/IF97-Rev.pdf
-------------------------------------------------
'Инженерные расчёты на Python'
https://zen.yandex.ru/id/5f33dcd5554adc5b33aaee83
https://medsv.github.io/dzen/
"""

import numpy as np

__author__ = "Sergey Medvedev"
__copyright__ = "Sergey Medvedev, 2020"
__license__ = "GPL"
__version__ = "1.2"
__maintainer__ = "Sergey Medvedev"
__email__ = "medsv@yandex.ru"
__status__ = "Production"

class SaturationCurve (object):
    """
    Линия насыщения водяного пара
    Отличие от версии 1.0: нижнее значение по давлению изменено с 611.213 на 611.212677
    """
    n = np.array([0.11670521452767E4, -0.72421316703206E6, -0.17073846940092E2, 0.12020824702470E5,
        -0.32325550322333E7, 0.14915108613530E2, -0.48232657361591E4, 0.40511340542057E6,
        -0.23855557567849, 0.65017534844798E3], dtype=float)

    def __init__(self):
        """
        Инициализация граничных значений параметров
        """
        self.T_min = 273.15   # Минимальное значение температуры, K
        self.T_max = 647.096  # Максимальное значение температуры, K
        self.p_min = 611.212677  # Минимальное значение давления, Па
        self.p_max = 22.064e6  # Максимальное значение давления, Па

    def p_T(self, T):
        """
        Определение давления насыщения (Па) по заданной температуре (К)
        T: температура, К
        return: абсолютное давление, Па
        """
        if not (self.T_in(T)):
            raise ValueError(f"Значение температуры должно находиться в диапазоне [{self.T_min} K; {self.T_max} K]")
        T = T + self.n[8] / (T - self.n[9])
        A = T * T + self.n[0] * T + self.n[1]
        B = self.n[2] * T * T + self.n[3] * T + self.n[4]
        C = self.n[5] * T * T + self.n[6] * T + self.n[7]
        p = (2 * C / (-B + (B * B - 4 * A * C) ** 0.5)) ** 4 * 1e6
        return p

    def p_t(self, t):
        """
        Определение давления насыщения (Па) по заданной температуре (C)
        t: температура, C
        return: абсолютное давление, Па
        """
        return self.p_T(t+273.15)

    def T_p(self, p):
        """
        Определение температуры насыщения (К) по заданному давлению (Па)
        p: абсолютное давление, Па
        return: температура, К
        """
        if not (self.p_in(p)):
            raise ValueError(f"Значение давления должно находиться в диапазоне [{self.p_min} Па; {self.p_max/1e6} МПа]")
        betta = (p / 1e6) ** 0.25
        E = betta * betta + self.n[2] * betta + self.n[5]
        F = self.n[0] * betta * betta + self.n[3] * betta + self.n[6]
        G = self.n[1] * betta * betta + self.n[4] * betta + self.n[7]
        D = 2 * G / (-F - (F * F - 4 * E * G) ** 0.5)
        T = (self.n[9] + D - ((self.n[9] + D) ** 2 - 4 * (self.n[8] + self.n[9] * D)) ** 0.5) / 2
        return T

    def t_p(self, p):
        """
        Определение температуры насыщения (C) по заданному давлению (Па)
        p: абсолютное давление, Па
        return: температура, C
        """
        return self.T_p(p) - 273.15

    def p_in(self, p):
        """
        Проверка нахождения значения давления внутри допустимого диапазона
        p: давление, Па
        return: True если давление находится внутри допустимого диапазона, False в противном сучае
        """
        return self.p_min <= p <= self.p_max

    def T_in(self, T):
        """
        Проверка нахождения значения температуры внутри допустимого диапазона
        T: температура, К
        return: True если температура находится внутри допустимого диапазона, False в противном сучае
        """
        return self.T_min <= T <= self.T_max

    def t_in(self, t):
        """
        Проверка нахождения значения температуры внутри допустимого диапазона
        t: температура, C
        return: True если температура находится внутри допустимого диапазона, False в противном сучае
        """
        return self.T_in(t + 273.15)
