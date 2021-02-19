from random import randint
from mpmath import besseli
import numpy as np
from Draw import Draw
from scipy import special

from Noise import Noise
from Signal import Signal
from Cos import Cos


class Optimal_Detector(Signal):
    def __init__(self):
        self.information = "Я"
        self.information_bit = None
        self.analog_signal_to_send = []
        self.time_signal = []
        self.N = 0
        self.analog_signal_with_noise = []
        self.time_to_result = []


    def run(self):
        print("мы отправили текст {Я}")
        self.information_bit = self.text_to_bits(text=self.information)
        print(self.information_bit)
        self.create_signal()
        self.counts = self.analog_signal_with_noise[::100]
        self.time_counts =  self.time_signal[::100]
        self.show_signal_to_send()
        self.decoder()
    def text_to_bits(self, text, encoding='utf-8', errors='surrogatepass'):
        bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
        return str(bits.zfill(8 * ((len(bits) + 7) // 8)))

    def decoder(self):
        self.time_to_result = list(range(0, 2 * (len(self.information_bit)), 2))
        new_func = []

        for i, simvol in enumerate(self.information_bit):
            t = self.time_to_result[i]
            cos_oporn = Cos(phase=0, start_piece=t, t_start=t, t_end=t + 2, end_piece=t + 2)
            cos_oporn.create_signal()
            signal = self.analog_signal_with_noise[i*self.N:(i+1)*self.N]
            print(len(cos_oporn.analog[1]), len(signal))
            for i in range(len(signal)):
                new_func.append(signal[i]*cos_oporn.analog[1][i])
        Draw(func=new_func, time=self.time_signal,
             title=f"Приняли сигнал * cos(wt)",
             xlabel="t [мс]", ylabel="V [мВ]",
             main_dir_name="Корреляционный обнаружитель").draw()

    def create_signal(self):
        self.time_to_result = list(range(0, 2 * (len(self.information_bit)), 2))
        for i, simvol in enumerate(self.information_bit):
            t = self.time_to_result[i]
            if simvol == "1":
                Sin_0 = Cos(phase=3.14 / 2, start_piece=t, t_start=t, t_end=t + 2, end_piece=t + 2)
                Sin_0.create_signal()
                self.analog_signal_with_noise += (Sin_0.analog_with_noise[1])
                self.analog_signal_to_send += (Sin_0.analog[1])
                self.time_signal += list(Sin_0.analog_with_noise[0])

            if simvol == '0':
                Cos_1 = Cos(phase=0, start_piece=t, t_start=t, t_end=t + 2, end_piece=t + 2)
                Cos_1.create_signal()
                self.analog_signal_with_noise += (Cos_1.analog_with_noise[1])
                self.analog_signal_to_send += (Cos_1.analog[1])
                self.time_signal += list((Cos_1.analog_with_noise[0]))
        self.N = len(self.analog_signal_with_noise)//len(self.information_bit)
    def show_signal_to_send(self):
        Draw(func=self.analog_signal_to_send, time=self.time_signal,
             title=f"Передаем текст  - Я - ДО ШУМА",
             xlabel="t [мс]", ylabel="V [мВ]",
             main_dir_name="Корреляционный обнаружитель").draw()
        Draw(func=self.analog_signal_with_noise, time=self.time_signal,
             title=f"Передаем текст  - Я - ПОСЛЕ ШУМА",
             xlabel="t [мс]", ylabel="V [мВ]",
             main_dir_name="Корреляционный обнаружитель").draw()
        Draw(
             count_3=self.counts, t_count_3=self.time_counts,
             title=f"выборка которую мы делаем на приемной стороне",
             xlabel="t [мс]", ylabel="V [мВ]",
             main_dir_name="Корреляционный обнаружитель").draw()
