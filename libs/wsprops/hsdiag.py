"""
В модуле размещён класс HSDiag, содержащий методы для расчёта теплофизических свойств воды и водяного пара (области 1, 2 и частично 4)
Допустимый диапазон далений для области 4: 611,213 Па - 16,529 МПа
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
__email__ = "engpython@yandex.ru"
__status__ = "Production"

from .region4 import Region4

class HSDiag():
    """
    Класс для расчёта теплофизических свойств воды и водяного пара
    """
    def __init__(self):
        """
        Инициализация параметров
        """        
        self.region4 = Region4()
        self.region1 = self.region4.region1
        self.region2 = self.region4.region2
        self.sc = Region4.sc
        self.regions = [self.region1, self.region2, self.region4]
        self.curReg = None

    def props_Tp(self, T, p):
        """
        Расчёт теплофизических свойств воды и водяного пара по температуре и давлению.
        T: температура, К
        p: давление, Па
        return: словарь свойств
        """
        self.curReg = None
        for region in self.regions:
            if region.Tp_in(T, p):
                self.curReg = region
                return region.props_Tp(T, p)
        self.__error(f"T={T} К, p={p} Па")

    def props_tp(self, t, p):
        """
        Расчёт теплофизических свойств воды и водяного пара по температуре и давлению.
        t: температура, C
        p: давление, Па
        return: словарь свойств
        """        
        for region in self.regions:
            self.curReg = None
            if region.tp_in(t, p):
                self.curReg = region
                return region.props_Tp(t + 273.15, p)
        self.__error(f"t={t} С, p={p} Па")

    def props_ph(self, p, h):
        """
        Расчёт теплофизических свойств воды и водяного пара по давлению и энтальпии.
        p: давление, Па
        h: энтальпия, Дж/кг
        return: словарь свойств
        """
        self.curReg = None
        for region in self.regions:
            if region.ph_in(p, h):
                self.curReg = region
                return region.props_ph(p, h)
        self.__error(f"p={p} Па, h={h} Дж/кг")

    def props_ps(self, p, s):
        """
        Расчёт теплофизических свойств воды и водяного пара по давлению и энтропии.
        p: давление, Па
        s: энтропия, Дж/кг/К
        return: словарь свойств.
        """
        self.curReg = None       
        for region in self.regions:
            if region.ps_in(p, s):
                self.curReg = region
                return region.props_ps(p, s)
        self.__error(f"p={p} Па, s={s} Дж/кг/К")  

    def props_px(self, p, x):
        """
        Расчёт теплофизических свойств влажного водяного пара по давлению и степени сухости.
        p: давление, Па
        x: степень сухости x = [0; 1]
        return: словарь свойств.
        """
        self.curReg = None         
        if self.region4.px_in(p, x):
            self.curReg = self.region4
            return self.region4.props_px(p, x)
        self.__error(f"p={p} Па, x={x}")

    def props_p(self, p):
        """
        Расчёт теплофизических свойств кипящей воды и сухого насыщенного пара при давлении p
        p: давление, Па
        return: кортеж двух словарей: 0 - кипящая вода, 1 - сухой насыщенный пар
        """
        self.curReg = None
        if self.region4.p_in(p):
            self.curReg = self.region4
            return self.region4.props_p(p)
        self.__error(f"p={p} Па")

    def p_T(self, T):
        """
        Определение давления насыщения (Па) по заданной температуре (К)
        T: температура, К
        return: абсолютное давление, Па
        """
        if self.sc.T_in(T):
            return self.sc.p_T(T)
        self.__error(f"T={T} К")

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
        if self.sc.p_in(p):
            return self.sc.T_p(p)
        self.__error(f"p={p} Па")  

    def t_p(self, p):
        """
        Определение температуры насыщения (C) по заданному давлению (Па)
        p: абсолютное давление, Па
        return: температура, C
        """
        return self.T_p(p) - 273.15

    def dh_p(self, p):
        """
        Расчёт скрытой теплоты парообразования (h'' - h')
        p: давление, Па
        return: скрытая теплота парообразования, Дж/кг
        """
        if self.sc.p_in(p):
            return self.region4.dh_p(p)
        self.__error(f"p={p} Па")
    
    def ds_p(self, p):
        """
        Расчёт значения s'' - s'
        p: давление, Па
        return: значение s'' - s', Дж/кг/К
        """
        if self.sc.p_in(p):
            return self.region4.ds_p(p)
        self.__error(f"p={p} Па")

    def __error(self, str):
        """
        Генерация исключения
        str: описание причины возникновения исключения 
        return: значение s'' - s', Дж/кг/К
        """        
        raise ValueError("Значения параметров " + str + " лежат вне допустимой области.")
