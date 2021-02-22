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
        self.sigma=0.001

        self.information_bit_result = []
        self.information_bit_result_signal = []

        self.new_bits = []

        self.count_akf = []
        self.time_akf = []


    def run(self):
        print(f"мы отправили текст {self.information}")
        self.information_bit = self.text_to_bits(text=self.information)
        print(f"{self.information}- представляется в битах - ", self.information_bit)
        self.text_from_bits(bits=self.information_bit)
        self.create_signal()
        self.counts = self.analog_signal_with_noise[::100]
        self.time_counts= self.time_signal[::100]
        self.show_signal_to_send()
        self.decoder()
    def text_to_bits(self, text, encoding='utf-8', errors='surrogatepass'):
        bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
        return str(bits.zfill(8 * ((len(bits) + 7) // 8)))

    def decoder(self):

        self.time_to_result = list(range(0, 2 * (len(self.information_bit)), 2))
        signal_with_noise_reception = []
        for i, simvol in enumerate(self.information_bit):
            t = self.time_to_result[i]
            cos_oporn = Cos(phase=0, start_piece=t, t_start=t, t_end=t + 2, end_piece=t + 2)
            cos_oporn.create_signal()
            bit_signal = self.analog_signal_with_noise[i*self.N:(i+1)*self.N]
            for i in range(len(bit_signal)):
                si = bit_signal[i]*cos_oporn.analog[1][i]
                signal_with_noise_reception.append(si)

        '''
        Draw(func=signal_with_noise_reception, time=self.time_signal,
             count_3=signal_with_noise_reception[::100], t_count_3=self.time_counts,
             title=f"Приняли сигнал * cos(wt)",
             xlabel="t [мс]", ylabel="V [мВ]",
             main_dir_name="Корреляционный обнаружитель").draw()
            '''
        rec_oporn = Rectangle(phase=0, start_piece=0, t_start=0, t_end=2, end_piece=2)
        rec_oporn.create_signal()

        x = signal_with_noise_reception[::100]
        s = rec_oporn.counts[1]
        kol_vo_count = len(x)//len(self.information_bit)
        corr = []

        for i, t in enumerate(x):
            sum = 0

            for j, si in enumerate(s):
                if j + i >= len(x):
                    sum += 0
                else:
                    sum += si * x[j + i]
            corr.append(sum)


            if (i % kol_vo_count == 0 and i!=0) or i==len(x)-1:
                self.porog(Energy=self.E, corr=corr[i-kol_vo_count: i])





        Draw(func=corr, time=self.time_counts,
             count_3=corr[::16], t_count_3=self.time_counts[::16],
             title=f"После коррелятора",
             xlabel="t [мс]", ylabel="V [мВ]",
             main_dir_name="Корреляционный обнаружитель").draw()

        Draw(func=self.information_bit_result, time=self.time_counts,
             count_3=self.count_akf, t_count_3=range(0, 2*len(self.information_bit), 2),
             title=f"Принятие решения",
             xlabel="t [мс]", ylabel="V [мВ]",
             main_dir_name="Корреляционный обнаружитель").draw()

        self.new_bits = self.information_bit_result[::16]
        print("Получили - ", self.new_bits)
        bits=''
        for x in self.information_bit_result[::16]:
            bits+=str(x)
        self.ver_osch()
        #print("Перевод в текст :", self.text_from_bits(bits))
    def ver_osch(self):
        n=0
        for i in range(len(self.information_bit)):
            if int(self.information_bit[i]) == int(self.new_bits[i]):
                n+=1
        print("Процент правильного обнаружения бит", n/len(self.information_bit))

    def text_from_bits(self, bits, encoding='utf-8', errors='surrogatepass'):
        n = int(bits, 2) #переводит строку из нулей и единиц в целое число
        a = hex(n)#переводит его на строку в шестнадцатеричной системе
        x = a[2:]#Первые 2 символы (0x) нужно удалить:
        print(x)
        v = bytes.fromhex(x) #Теперь эту строку возможно применить как аргумент метода bytes.fromhex(), чтобы получить объект типа bytes


        return bytes.decode(v, encoding='utf-8',errors=errors)


    def create_signal(self):
        self.time_to_result = list(range(0, 2 * (len(self.information_bit)), 2))
        for i, simvol in enumerate(self.information_bit):
            t = self.time_to_result[i]
            if simvol == "0":
                Cos_0 = Cos(sigma=self.sigma, phase=3.14, start_piece=t, t_start=t, t_end=t + 2, end_piece=t + 2)
                Cos_0.create_signal()
                self.E = Cos_0.Energy
                self.analog_signal_with_noise += (Cos_0.analog_with_noise[1])
                self.analog_signal_to_send += (Cos_0.analog[1])
                self.time_signal += list(Cos_0.analog_with_noise[0])

            if simvol == '1':
                Cos_1 = Cos(sigma=self.sigma,phase=0, start_piece=t, t_start=t, t_end=t + 2, end_piece=t + 2)
                Cos_1.create_signal()
                self.E = Cos_1.Energy
                self.analog_signal_with_noise += (Cos_1.analog_with_noise[1])
                self.analog_signal_to_send += (Cos_1.analog[1])
                self.time_signal += list((Cos_1.analog_with_noise[0]))
        self.N = len(self.analog_signal_with_noise)//len(self.information_bit)
    def show_signal_to_send(self):
        pass
        '''
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
        '''

    def porog(self, corr, Energy):
        gamma = special.erfinv(self.alfa) * self.sigma * Energy ** 0.5


        for i, x in enumerate(corr):

            if x >= gamma:
                #print(1, end="")
                self.information_bit_result.append(1)
                if i==0:
                    self.count_akf.append(1)

            else:
                #print(0, end="")
                self.information_bit_result.append(0)
                if i==0:
                    self.count_akf.append(0)






