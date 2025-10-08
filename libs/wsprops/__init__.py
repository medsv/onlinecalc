"""
Пакет содержащий классы для расчёта теплофизических свойств воды и водяного пара
Методики расчёта взяты из документов
http://www.iapws.org/relguide/IF97-Rev.pdf
http://www.iapws.org/relguide/visc.pdf
-------------------------------------------------
'Инженерные расчёты на Python'
https://zen.yandex.ru/id/5f33dcd5554adc5b33aaee83
https://medsv.github.io/
"""

__author__ = "Сергей Медведев"
__copyright__ = "Сергей Медведев, 2020-2021"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Сергей Медведев"
__email__ = "medsv@yandex.ru"
__status__ = "Production"

from .hsdiag import HSDiag  # Основной (сводный) расчётный класс
from .region1 import Region1  # Область 1
from .region2 import Region2  # Область 2
from .region4 import Region4  # Область 4
from .saturationcurve import SaturationCurve  # Линия насыщения
from .visc import Visc  # Расчёт динамической и кинематической вязкости
