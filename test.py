'''a = ['1', '2', '3', '4']
priznok = 2
t = a.pop(priznok)
a.insert(1, t)

t = a.pop(1)
a.insert(priznok, t)
print(a)
'''

'''with open('', 'r', encoding='utf-16') as t:
    matr = t.read().split('\n')
    matr.remove('')
    for i in range(len(matr)):
        matr[i] = matr[i].split()
        key = matr[i].pop(1)
        matr[i].insert(0, key)
    print(matr)

    matr = sorted(matr)
    for i in range(len(matr)):
        key = matr[i].pop(0)
        matr[i].insert(1, key)
    print(matr)
    matr.reverse()
    print(matr)
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
#
# def f():
#     x = [0, 10, 5, 15, 20]
#     y1 = [1, 7, 3, 5, 11]
#     y2 = [4, 3, 1, 8, 12]
#     plt.figure(figsize=(12, 7))
#     plt.plot(x, y1, 'o-r', alpha=0.7, label="first", lw=5, mec='b', mew=2, ms=10)
#     plt.plot(x, y2, 'v-.g', label="second", mec='r', lw=2, mew=2, ms=12)
#     plt.legend()
#     plt.grid(True)
#
#      #задаем размер шрифта
#     matplotlib.rcParams.update({'font.size': 12})
#
#     rg = np.random.Generator(np.random.PCG64(11))
#     x = np.arange(6)
#     y = rg.poisson(149, x.size)
#     yerr = [
#         0.7*np.sqrt(y),
#         1.2*np.sqrt(y)
#     ]
#     plt.errorbar(x, y, yerr=yerr, marker='o', linestyle='none',
#         ecolor='k', elinewidth=0.8, capsize=4, capthick=1)
#
#     # добавляем заголовок диаграммы
#     plt.title(r' Ваш кошелёк за последнее время')
#
#     # задаем диапазон значений оси y
#     plt.ylim([0, 20])
#     # оптимизируем поля и расположение объектов
#     plt.tight_layout()
#
#     plt.xlim([10, 20])  # диапазон горизонтальной оси от 10 до 20
#     plt.xlim([0, 15])    # диапазон вертикальной оси от 0 до 15
#     plt.xlabel('финансы (руб) ', fontsize=16)
#     plt.ylabel(r' Время ', fontsize=16)
#     plt.show()
# f()

# import time
# import utilities as u
# print(time.ctime(13213242))
# print(u.time_shorting(time.ctime(13213242)))

from currency_converter import CurrencyConverter
from decimal import Decimal

c=CurrencyConverter()

print(round(Decimal(c.convert(94, 'RUB', 'EUR')),2))
