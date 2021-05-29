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

n = 5
if n == 1:
    Correlation_Detector(function=Triangle, start_piece=0, t_start=2, t_end=4, end_piece=6).study()
    Correlation_Detector(function=Rectangle, start_piece=1, t_start=2, t_end=4, end_piece=5).study()
    Noise().show_noise()
if n == 2:
    Optimal_Detector().run()
if n==3:
    import random
    A = random.randrange(5, 15, 1)/10
    rec_ideal = Rectangle(A=1)
    rec_ideal.create_signal()
    rec_real = Rectangle(A=A)
    rec_real.create_signal()
    T = 0
    E = 0
    for i in range(len(rec_ideal.counts[1])):
        T += rec_ideal.counts[1][i]*rec_real.counts_with_noise[1][i]
        E += rec_ideal.counts[1][i]*rec_ideal.counts[1][i]
    a_m = T/E
    print(a_m)
    print(A)
    Draw(func=rec_ideal.counts[1], time=rec_real.counts[0],
         title=f"Детерминированный сигнал",
         xlabel="t [мс]", ylabel="V [В]",).draw()
    Draw(func=rec_real.counts[1], time=rec_real.counts[0],
         title=f"Сигнал с неизвестной амплитой",
         xlabel="t [мс]", ylabel="V [В]", ).draw()

if n ==4:
    import random

    bits = "01"
    ygol = 280/180*3.14#random.randrange(0, 2*314, 1) / 100
    def fCos(bits,pfi):
        analog_signal_with_noise=[]
        analog_signal_to_send=[]
        counts_signal_to_send=[]
        counts_signal_with_noise=[]
        sigma = 0.5
        E=0
        time_analog=[]
        time_counts=[]
        time_to_result = list(range(0, 2 * (len(bits)), 2))
        for i, bit in enumerate(bits):
            t = time_to_result[i]
            if bit == "0":
                Cos_0 = Cos(sigma=sigma, phase=pfi, start_piece=t, t_start=t, t_end=t+2, end_piece=t+2, A=1)
                Cos_0.create_signal()
                E += Cos_0.Energy

                analog_signal_to_send += (Cos_0.analog[1])
                analog_signal_with_noise += [x + y for x, y in zip(Cos_0.analog[1],
                                                                   sigma * np.random.randn(len(Cos_0.analog[1])))]
                counts_signal_to_send += Cos_0.counts[1]
                counts_signal_with_noise += [x + y for x, y in zip(Cos_0.counts[1], sigma * np.random.randn(len(Cos_0.counts[1])))]
                time_analog+=list(Cos_0.analog_with_noise[0])
                time_counts+=list(Cos_0.counts_with_noise[0])


            if bit == '1':
                Cos_1 = Cos(sigma=sigma, phase=3.14+pfi, start_piece=t, t_start=t, t_end=t+2, end_piece=t+2, A=1)
                Cos_1.create_signal()
                E += Cos_1.Energy
                analog_signal_to_send += (Cos_1.analog[1])
                analog_signal_with_noise += [x + y for x, y in zip(Cos_1.analog[1], sigma * np.random.randn(len(Cos_1.analog[1])))]

                counts_signal_to_send += Cos_1.counts[1]
                counts_signal_with_noise += [x + y for x, y in zip(Cos_1.counts[1], sigma * np.random.randn(len(Cos_1.counts[1])))]

                time_analog += list(Cos_1.analog_with_noise[0])
                time_counts += list(Cos_1.counts_with_noise[0])


        return (time_counts, counts_signal_to_send,counts_signal_with_noise), (time_analog, analog_signal_to_send, analog_signal_with_noise), E


    def draw(pfi, title):
        (time_counts, counts_signal_to_send,counts_signal_with_noise), (time_analog, analog_signal_to_send, analog_signal_with_noise), E = fCos(
            bits, pfi)
        Draw(func=analog_signal_with_noise, time=time_analog,
             count=counts_signal_with_noise, t_count=time_counts,
             title=title,
             xlabel="t [мс]", ylabel="V [мВ]", ).draw()


    m = 4
    tets = list(set([x//100 for x in range(0,2*314,314//m)]))
    print("sigma = 0.5")
    print( "Набор прототипов сигналов с начальными фазами:")
    print(*[x*180//3.14 for x in  tets], "градусов")
    draw(pfi=0, title="Исходный сигнал")
    draw(pfi=ygol, title="Сигнал с неизвестной фазой")

    T=[]
    import numpy as np
    import matplotlib.pyplot as plt


    ac=[]
    (time_counts_, counts_signal_to_send_,counts_signal_with_noise_), (time_analog_, analog_signal_to_send_, analog_signal_with_noise_), E_ = fCos(
        bits, ygol)
    print("осш ", E_ ** 0.5 / 0.5)
    fig, axes = plt.subplots(4,2)

    axes[0][0].plot(time_counts_, counts_signal_with_noise_, 'ro')
    axes[0][0].plot(time_analog_, analog_signal_with_noise_, )
    axes[0][0].set_title(r'Сигнал c неизвестной фазой')
    axes[0][0].grid(True)
    k=0
    j=1
    for i,tet in enumerate(tets):
        (time_counts,counts_signal_to_send, counts_signal_with_noise_), (time_analog, analog_signal_to_send, analog_signal_with_noise), E = fCos(
            bits, tet)
        c = np.correlate(time_counts, counts_signal_with_noise_, 'full')
        ac.append(c)
        axes[k][j].plot(time_counts_,counts_signal_with_noise_,'bo')
        axes[k][j].plot(time_analog, analog_signal_with_noise, )
        axes[k][j].text(0 ,0, f'фаза {tet*180//3.14}')
        axes[k][j].grid(True)
        if i%2==0:
            j=0
            k+=1
        else:
            j=1
    plt.show()

    fig, axes = plt.subplots(4, 2)

    axes[0][0].plot(time_counts_, counts_signal_with_noise_, 'ro')
    axes[0][0].plot(time_analog_, analog_signal_with_noise, )
    axes[0][0].set_title(r'Сигнал c неизвестной фазой')
    axes[0][0].grid(True)
    k = 0
    j = 1
    for i, c_ in enumerate(ac):
        axes[k][j].plot(np.arange(-4+0.125, 4, 0.125),c_)
        axes[k][j].text(-4, 10, f'фаза {tets[i] * 180 // 3.14}')
        axes[k][j].grid(True)
        if i % 2 == 0:
            j = 0
            k += 1
        else:
            j = 1

    a=[x[len(ac)//2] for x in ac]
    i = a.index(max(a))
    print("Сигнал с наибольшей корреляцией в нуле c фазой", end=' = ')
    print(tets[i]* 180 // 3.14, "градусов (наша оценка)")
    print(f"случайная начальная фаза сигнала, {(ygol* 180 // 3.14)} град")
    plt.show()
if n==5:

