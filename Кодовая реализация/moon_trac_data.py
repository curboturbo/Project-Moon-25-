import numpy as np
import matplotlib.pyplot as plt
"""ОТРИСОВКА ГРАФИКОВ ЛУННОГО СПУСКА, ascendCords- КСП , temp.txt,my_coords - ДАННЫЕ ИЗ МАТ МОДЕЛИ(test.py,landing.py)"""

f = open(r"ascendCords (1).txt").readlines()
f1 = []
for i in range(len(f)):
    if f[i]=='\n':
        pass
    else:
        f1.append(float(f[i][0:-1]))
time_ksp = [i/4 for i in range(len(f1))]
f2 = open('my_coords.txt').read()
f2 = [float(i) for i in f2.split()]
f3 = open('temp.txt').read()
f3 = [float(i) for i in f3.split()]
time_f2 = [i/10_000 for i in range(len(f2)+len(f3))]
f3+=f2
plt.plot(time_ksp,f1,color='blue',label = "KSP")
plt.plot(time_f2,f3,color='red',label = "Мат.модель")
plt.xlabel('Время спуска с предпосадочной орбиты (сек)') 
plt.ylabel('Высота под Луной-25 (метры)')
plt.legend(loc='best', fontsize=12, title_fontsize='large')
plt.grid(True)
plt.show()