import base64
from random import randint
from mpmath import besseli
import numpy as np
from Draw import Draw
from scipy import special
from Noise import Noise
from Rectangle import Rectangle
from Signal import Signal
from scipy import signal
from Cos import Cos
import matplotlib.pyplot as plt
import statistics
import codecs
from scipy.stats import norm
class Optimal_Detector(Signal):
    def __init__(self):
        self.information = "Я"
        self.information_bit = None
        self.analog_signal_to_send = []
        self.time_signal = []
        self.N = 0
        self.analog_signal_with_noise = []
        self.time_to_result = []
        self.E =0
        self.alfa = 0.2
        self.sigma=5

        self.information_bit_result = []
        self.information_bit_result_signal = []

        self.new_bits = []

        self.count_akf = []
        self.time_akf = []


    def run(self):
        print(f"мы отправили текст {self.information}")
        print("sigma=", self.sigma)

        self.information_bit = self.text_to_bits(text=self.information)
        print(f"{self.information} - представляется в битах - ", self.information_bit)
        self.text_from_bits(bits=self.information_bit)
        self.create_signal()
        print("ОСШ",self.E**0.5/ self.sigma)
        otvet = self.statik()
        print(f"результат на входе приемника {otvet}")
        self.xarakteristik()
    def text_to_bits(self, text, encoding='utf-8', errors='surrogatepass'):
        bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
        return str(bits.zfill(8 * ((len(bits) + 7) // 8)))


    def text_from_bits(self, bits, encoding='utf-8', errors='surrogatepass'):
        n = int(bits, 2) #переводит строку из нулей и единиц в целое число
        a = hex(n)#переводит его на строку в шестнадцатеричной системе
        x = a[2:]#Первые 2 символы (0x) нужно удалить:
        v = bytes.fromhex(x) #Теперь эту строку возможно применить как аргумент метода bytes.fromhex(), чтобы получить объект типа bytes
        return bytes.decode(v, encoding='utf-8',errors=errors)


    def create_signal(self):
        self.time_to_result = list(range(0, 2 * (len(self.information_bit)), 2))
        for i, simvol in enumerate(self.information_bit):
            t = self.time_to_result[i]
            if simvol == "0":
                Rec_0 = Rectangle(sigma=self.sigma, phase=0, start_piece=t, t_start=t, t_end=t + 2, end_piece=t + 2, A=-1)
                Rec_0.create_signal()
                self.E += Rec_0.Energy
                self.analog_signal_with_noise += (Rec_0.analog_with_noise[1])
                self.analog_signal_to_send += (Rec_0.analog[1])
                self.time_signal += list(Rec_0.analog_with_noise[0])

            if simvol == '1':
                Rec_1 = Rectangle(sigma=self.sigma,phase=0, start_piece=t, t_start=t, t_end=t + 2, end_piece=t + 2, A=1)
                Rec_1.create_signal()
                self.E += Rec_1.Energy
                self.analog_signal_with_noise += (Rec_1.analog_with_noise[1])
                self.analog_signal_to_send += (Rec_1.analog[1])
                self.time_signal += list((Rec_1.analog_with_noise[0]))

        self.counts = self.analog_signal_with_noise[::100]
        self.time_counts = self.time_signal[::100]
    def show_signal_to_send(self):

        Draw(func=self.analog_signal_to_send, time=self.time_signal,
             title=f"Передаем текст  - {self.information} - ДО ШУМА",
             xlabel="t [мс]", ylabel="V [мВ]",
             main_dir_name="Корреляционный обнаружитель").draw()
        Draw(func=self.analog_signal_with_noise, time=self.time_signal,
             title=f"Передаем текст  - {self.information}  - ПОСЛЕ ШУМА",
             xlabel="t [мс]", ylabel="V [мВ]",
             main_dir_name="Корреляционный обнаружитель").draw()

        Draw(func=self.analog_signal_with_noise, time=self.time_signal,
             count_3=self.counts, t_count_3=self.time_counts,
             title=f"выборка которую мы делаем на приемной стороне",
             xlabel="t [мс]", ylabel="V [мВ]",
             main_dir_name="Корреляционный обнаружитель").draw()
    def statik(self):

        Rec_0 = Rectangle(sigma=self.sigma, phase=0, start_piece=0, t_start=0, t_end=2, end_piece=2, A=-1)
        Rec_1 = Rectangle(sigma=self.sigma, phase=0, start_piece=0, t_start=0, t_end=2, end_piece=2, A=1)
        Rec_0.create_signal()
        Rec_1.create_signal()
        self.N = len(self.counts) // len(self.information_bit)
        T0 = 0
        T1 = 0
        T_0=[]
        T_1 = []
        bits=''
        for i in range(len(self.counts)):
            if i % self.N!=0 or i==0:
                T0 += self.counts[i]*Rec_0.counts_with_noise[1][i//self.N]
                T1 += self.counts[i] * Rec_1.counts_with_noise[1][i // self.N]
                T_0.append(T0)
                T_1.append(T1)
            else:
                T_0.append(0)
                T_1.append(0)
                if T0 - Rec_0.Energy/2 > T1 - Rec_1.Energy/2:
                    bits=bits+'0'
                else:
                    bits = bits + '1'
                T0 = 0
                T1 = 0
        else:

            if T0 - Rec_0.Energy > T1 - Rec_1.Energy:
                bits=bits+'0'
            else:
                bits = bits + '1'
        Draw(func=T_0, time=self.time_counts,
             func_2=T_1, time_2=self.time_counts,
             flabel="T0", flabel_2="T1",
             xlabel="t [мс]", ylabel="мкВ",
             title="Статистики во времени").draw()
        Draw(func=[x-y for x,y in zip(T_1, T_0)], time=self.time_counts,
             flabel="T1-T0",
             xlabel="t [мс]", ylabel="мкВ",
             title="Разность статистик во времени").draw()
        return bits



    def xarakteristik(self):
        d = [x for x in np.arange(0.1, 8, 0.5)]  # Отношение сигнал/шум
        E = self.E/len(self.information_bit)
        x = 1 - norm.cdf(d)
        sigma = [(E) ** 0.5 / x for x in d]
        D=[]

        for k, s in enumerate(sigma):  # Эксперимент
            Rec_0 = Rectangle(sigma=s, phase=0, start_piece=0, t_start=0, t_end=2, end_piece=2, A=-1)
            Rec_1 = Rectangle(sigma=s, phase=0, start_piece=0, t_start=0, t_end=2, end_piece=2, A=1)
            Rec_0.create_signal()
            Rec_1.create_signal()
            N = 1000  # кол-во эксп-ов
            m = 0
            for i in range(N):
                sk1 = Rec_0.counts[1]
                sk2 = Rec_1.counts[1]
                xk1 = [x + y for x, y in zip(sk1, s * np.random.randn(len(sk1)))]  # Cигнал + шум с sigma=s
                xk2 = [x + y for x, y in zip(sk2, s * np.random.randn(len(sk2)))]
                T11 = -E/2
                T12 = -E/2
                for j in range(len(sk1)):
                    T11 += sk1[j] * xk1[j]
                    T12 += sk2[j] * xk1[j]
                T21 = -E/2
                T22 = -E/2
                for j in range(len(sk2)):
                    T21 += sk1[j] * xk2[j]
                    T22 += sk2[j] * xk2[j]

                if T11 < T12 or T22<T21:
                    m += 1
            D.append(m / N/2)


        Draw(func=x, time=d,
             count_3=D, t_count_3=d,
             title=f"Вероятность ошибки Pош",
             xlabel="ОСШ[раз]", ylabel="%",).draw()

