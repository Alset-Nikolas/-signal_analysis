import numpy as np

from Draw import Draw

print("Start import")
from Cos import Cos
from Noise import Noise
from Rectangle import Rectangle
from Triangle import Triangle

print("Start import")

from Optimal_Detector import Optimal_Detector

from Correlation_Detector import Correlation_Detector

print("=" * 100)
print("\t\tИдет загрузка!")
print("=" * 100)

n = 1
if n == 1:
    #Correlation_Detector(sigma=0.65,function=Triangle, start_piece=0, t_start=2, t_end=4, end_piece=6).study()
    Correlation_Detector(sigma=0.65,function=Rectangle, start_piece=1, t_start=2, t_end=4, end_piece=5).study()
    #Noise().show_noise()
if n == 2:
    Optimal_Detector().run()
if n == 3:
    import random
    d=5
    A = random.randrange(5, 15, 1) / 10
    rec_ideal = Rectangle(A=1)
    rec_ideal.create_signal()
    rec_real = Rectangle(A=A)
    rec_real.create_signal()
    sigma = rec_real.Energy**0.5/d
    x1 = [x + y for x, y in zip(rec_real.counts[1], sigma * np.random.randn(len(rec_real.counts[1])))]
    x2 = [x + y for x, y in zip(rec_real.analog[1], sigma * np.random.randn(len(rec_real.analog[1])))]

    T = 0
    E = 0
    for i in range(len(rec_ideal.counts[1])):
        T += rec_ideal.counts[1][i] * x1[i]
        E += rec_ideal.counts[1][i] * rec_ideal.counts[1][i]
    a_m = T / E
    print(a_m)
    print(A)
    Draw(func=rec_ideal.counts[1], time=rec_real.counts[0],
         title=f"Детерминированный сигнал",
         xlabel="t [мс]", ylabel="V [В]", ).draw()
    Draw(func=x2, time=rec_real.analog[0],
         count=x1, t_count=rec_real.counts[0],
         title=f"Детерминированный сигнал",
         xlabel="t [мс]", ylabel="V [В]", ).draw()

    Draw(func=rec_real.counts[1], time=rec_real.counts[0],
         title=f"Сигнал с неизвестной амплитой",
         xlabel="t [мс]", ylabel="V [В]", ).draw()

if n == 4:
    import random

    bits = "01"
    ygol = 280 / 180 * 3.14  # random.randrange(0, 2*314, 1) / 100


    def fCos(bits, pfi):
        analog_signal_with_noise = []
        analog_signal_to_send = []
        counts_signal_to_send = []
        counts_signal_with_noise = []
        sigma = 0.5
        E = 0
        time_analog = []
        time_counts = []
        time_to_result = list(range(0, 2 * (len(bits)), 2))
        for i, bit in enumerate(bits):
            t = time_to_result[i]
            if bit == "0":
                Cos_0 = Cos(sigma=sigma, phase=pfi, start_piece=t, t_start=t, t_end=t + 2, end_piece=t + 2, A=1)
                Cos_0.create_signal()
                E += Cos_0.Energy

                analog_signal_to_send += (Cos_0.analog[1])
                analog_signal_with_noise += [x + y for x, y in zip(Cos_0.analog[1],
                                                                   sigma * np.random.randn(len(Cos_0.analog[1])))]
                counts_signal_to_send += Cos_0.counts[1]
                counts_signal_with_noise += [x + y for x, y in
                                             zip(Cos_0.counts[1], sigma * np.random.randn(len(Cos_0.counts[1])))]
                time_analog += list(Cos_0.analog_with_noise[0])
                time_counts += list(Cos_0.counts_with_noise[0])

            if bit == '1':
                Cos_1 = Cos(sigma=sigma, phase=3.14 + pfi, start_piece=t, t_start=t, t_end=t + 2, end_piece=t + 2, A=1)
                Cos_1.create_signal()
                E += Cos_1.Energy
                analog_signal_to_send += (Cos_1.analog[1])
                analog_signal_with_noise += [x + y for x, y in
                                             zip(Cos_1.analog[1], sigma * np.random.randn(len(Cos_1.analog[1])))]

                counts_signal_to_send += Cos_1.counts[1]
                counts_signal_with_noise += [x + y for x, y in
                                             zip(Cos_1.counts[1], sigma * np.random.randn(len(Cos_1.counts[1])))]

                time_analog += list(Cos_1.analog_with_noise[0])
                time_counts += list(Cos_1.counts_with_noise[0])

        return (time_counts, counts_signal_to_send, counts_signal_with_noise), (
        time_analog, analog_signal_to_send, analog_signal_with_noise), E


    def draw(pfi, title):
        (time_counts, counts_signal_to_send, counts_signal_with_noise), (
        time_analog, analog_signal_to_send, analog_signal_with_noise), E = fCos(
            bits, pfi)
        Draw(func=analog_signal_with_noise, time=time_analog,
             count=counts_signal_with_noise, t_count=time_counts,
             title=title,
             xlabel="t [мс]", ylabel="V [мВ]", ).draw()


    m = 4
    tets = list(set([x // 100 for x in range(0, 2 * 314, 314 // m)]))
    print("sigma = 0.5")
    print("Набор прототипов сигналов с начальными фазами:")
    print(*[x * 180 // 3.14 for x in tets], "градусов")
    draw(pfi=0, title="Исходный сигнал")
    draw(pfi=ygol, title="Сигнал с неизвестной фазой")

    T = []
    import numpy as np
    import matplotlib.pyplot as plt

    ac = []
    (time_counts_, counts_signal_to_send_, counts_signal_with_noise_), (
    time_analog_, analog_signal_to_send_, analog_signal_with_noise_), E_ = fCos(
        bits, ygol)
    print("осш ", E_ ** 0.5 / 0.5)
    fig, axes = plt.subplots(4, 2)

    axes[0][0].plot(time_counts_, counts_signal_with_noise_, 'ro')
    axes[0][0].plot(time_analog_, analog_signal_with_noise_, )
    axes[0][0].set_title(r'Сигнал c неизвестной фазой')
    axes[0][0].grid(True)
    k = 0
    j = 1
    for i, tet in enumerate(tets):
        (time_counts, counts_signal_to_send, counts_signal_with_noise_), (
        time_analog, analog_signal_to_send, analog_signal_with_noise), E = fCos(
            bits, tet)
        c = np.correlate(time_counts, counts_signal_with_noise_, 'full')
        ac.append(c)
        axes[k][j].plot(time_counts_, counts_signal_with_noise_, 'bo')
        axes[k][j].plot(time_analog, analog_signal_with_noise, )
        axes[k][j].text(0, 0, f'фаза {tet * 180 // 3.14}')
        axes[k][j].grid(True)
        if i % 2 == 0:
            j = 0
            k += 1
        else:
            j = 1
    plt.show()

    fig, axes = plt.subplots(4, 2)

    axes[0][0].plot(time_counts_, counts_signal_with_noise_, 'ro')
    axes[0][0].plot(time_analog_, analog_signal_with_noise, )
    axes[0][0].set_title(r'Сигнал c неизвестной фазой')
    axes[0][0].grid(True)
    k = 0
    j = 1
    for i, c_ in enumerate(ac):
        axes[k][j].plot(np.arange(-4 + 0.125, 4, 0.125), c_)
        axes[k][j].text(-4, 10, f'фаза {tets[i] * 180 // 3.14}')
        axes[k][j].grid(True)
        if i % 2 == 0:
            j = 0
            k += 1
        else:
            j = 1

    a = [x[len(ac) // 2] for x in ac]
    i = a.index(max(a))
    print("Сигнал с наибольшей корреляцией в нуле c фазой", end=' = ')
    print(tets[i] * 180 // 3.14, "градусов (наша оценка)")
    print(f"случайная начальная фаза сигнала, {(ygol * 180 // 3.14)} град")
    plt.show()
if n == 5:
    import numpy as np
    import random
    from scipy.stats import norm
    from scipy import special
    from sympy import marcumq

    fs = 2
    a_ = [0.1, 0.01, 0.001]


    ygol = random.randrange(0, 2 * 314, 1) / 100
    Cos_1 = Cos(f=2, phase=ygol, start_piece=0, t_start=0, t_end=0.5 * 4, end_piece=0.5 * 4, A=1)
    Cos_1.create_signal()
    Cos_1.print_data()
    n = len(Cos_1.counts[1])
    d = [x for x in np.arange(0.1, 8, 0.5)]  # Отношение сигнал/шум
    E = Cos_1.Energy
    sigma = [E ** 0.5 / x for x in d]
    q = [[] for x in range(len(a_))]
    for i, a in enumerate(a_):
        for s in sigma:
            P = 0
            gamma = np.log(1 / a) * n * s ** 2
            for _ in range(1000):
                x_counts = [x + y for x, y in zip(Cos_1.counts[1], s * np.random.randn(n))]

                Xc = 0
                Xs = 0
                for k in range(n):
                    Xc += 1 * x_counts[k] * np.cos(k * fs * 2 * np.pi * Cos_1.T)
                    Xs += 1 * x_counts[k] * np.sin(k * fs * 2 * np.pi * Cos_1.T)
                if Xc ** 2 + Xs ** 2 > gamma:
                    P += 1

            q[i].append(P / 1000)
    '''
    Q_T = []
    for j in range(len(sigma)):
        b = (n/(2*sigma[j]**2))**.5
        gamma = (np.log(1/a_[2])*n*sigma[j]**2)**.5
        Q_T.append(marcumq(1,b, round((2*np.log(1/a_[2]))**0.5,2)))
    print(Q_T)
    '''
    Q_T1 = [0.1003, 0.1409, 0.2411, 0.3951, 0.5774, 0.7481, 0.8745, 0.9487, 0.9830, 0.9954, 0.9990, 0.9998, 1.0000,
            1.0000,
            1.0000, 1.0000]
    Q_T2 = [0.0104, 0.0195, 0.0491, 0.1153, 0.2335, 0.4020, 0.5934, 0.7654, 0.8875, 0.9559, 0.9860, 0.9964,
            0.9993, 0.9999, 1.0000, 1.0000]
    Q_T3 = [0.0010, 0.0025, 0.0087, 0.0277, 0.0750, 0.1692, 0.3189, 0.5073, 0.6948, 0.8418, 0.9326,
            0.9767, 0.9935, 0.9986, 0.9997, 1.0000]
    _sigma = 0.7
    x_counts = [x + y for x, y in zip(Cos_1.counts[1], _sigma * np.random.randn(n))]
    x_analog = [x + y for x, y in zip(Cos_1.analog[1], _sigma * np.random.randn(len(Cos_1.analog[1])))]
    Draw(func=Cos_1.analog[1], time=Cos_1.analog[0],
         count=Cos_1.counts[1], t_count=Cos_1.counts[0],
         title='Квазидетерминированный сигнал',
         xlabel="t [мс]", ylabel="v [мВ]", ).draw()
    Draw(func=x_analog, time=Cos_1.analog[0],
         count=x_counts, t_count=Cos_1.counts[0],
         title=f'Квазидетерминированный сигнал в шуме ОСШ {E ** 0.5 / sigma}',
         xlabel="t [мс]", ylabel="v [мВ]", ).draw()
    Draw(func=Q_T1, time=d,
         func_2=Q_T2, time_2=d,
         func_3=Q_T3, time_3=d,
         count=q[0], t_count=d,
         count_2=q[1], t_count_2=d,
         count_3=q[2], t_count_3=d,
         flabel="Вероятность ложной тревоги 0.1",
         flabel_2='Вероятность ложной тревоги 0.01',
         flabel_3="Вероятность ложной тревоги 0.01",
         title='Характеристика обнаружения некогерентного приемника',
         xlabel="ОСШ [разы]", ylabel="Вероятность обнаружения [%]", ).draw()


    gamma = [-1 * special.ndtri(a_[0]) * (s ** 2 * E) ** 0.5 for s in sigma]
    K = []
    for j in range(len(sigma)):  # Теория
        x = 1 - norm.cdf((gamma[j] - E) / (sigma[j] * E ** 0.5))
        K.append(x)

    Draw(func=Q_T1, time=d,
         func_2=K, time_2=d,
         flabel="Некогерентный приемник",
         flabel_2='Когерентный приемник',
         title='Сравнение характеристик',
         xlabel="ОСШ [разы]", ylabel="Вероятность обнаружения [%]", ).draw()


