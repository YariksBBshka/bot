import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import utilities as u
import time



def get_a_graph(x,y1):
    x1=[0]
    c=0
    print(y1)
    for i in range(len(x)):

        if ((x1[-1]==(str(u.time_shorting(time.ctime(int(x[i]))))+f"\n({c})")) or (x1[-1]==str(u.time_shorting(time.ctime(int(x[i])))) )):
            c+=1
            x1.append(str(u.time_shorting(time.ctime(int(x[i]))))+f"\n({c})")
        else:
            c=0
            x1.append(str(u.time_shorting(time.ctime(int(x[i])))))
    x1.pop(0)
    print(x1)
    #x1=list(map(lambda r: u.time_shorting(time.ctime(int(r))), x))

    plt.figure(figsize=(12, 7))
    plt.plot(x1, y1, 'o-r', alpha=0.7, label="first", lw=5, mec='b', mew=2, ms=10)
    plt.legend()
    plt.grid(True)

     #задаем размер шрифта
    matplotlib.rcParams.update({'font.size': 12})

    rg = np.random.Generator(np.random.PCG64(11))
    x1 = np.arange(6)
    y = rg.poisson(149, x1.size)
    yerr = [
        0.7*np.sqrt(y),
        1.2*np.sqrt(y)
    ]
    plt.errorbar(x1, y, yerr=yerr, marker='o', linestyle='none',
        ecolor='k', elinewidth=0.8, capsize=4, capthick=1)

    # добавляем заголовок диаграммы
    plt.title(r' Ваш кошелёк за последнее время')

    # задаем диапазон значений оси y
    plt.ylim([min(y1), float(max(y1))*1.3])# какое-то число
    # оптимизируем поля и расположение объектов
    plt.tight_layout()


    plt.xlim([x1[0],x1[-1]])  # диапазон горизонтальной оси от 10 до 20

    plt.ylabel('Финансы (руб) ', fontsize=12)
    plt.xlabel(r' Время ', fontsize=12)

    plt.savefig('temp_graph.png')

