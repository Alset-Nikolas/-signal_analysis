from random import randint
from mpmath import besseli
import numpy as np
from Draw import Draw
from scipy import special

from Noise import Noise
from Signal import Signal
from Cos import Cos


class Optimal_Detector(Signal):
    def __init__(self, function=Cos):
        self.phase = randint(0, 360) * np.pi / 180
        self.phase_grad = self.phase * 180 / np.pi
        self.function = function(phase=self.phase)
        self.sigma = 0.01
        self.w = 2 * np.pi * self.function.fs

        self.hypothesis = [None, None]
        self.alfa = 0.2
        self.gamma = None
        self.gamma_level = None
        self.corr = [None, None]

        self.a = [0.2, 0.02, 0.002]

    def count_gamma(self):
        self.gamma = special.erfinv(self.alfa) * self.function.sigma * self.function.Energy ** 0.5

    def study(self):
        self.function.create_signal()
        self.cor()
        self.porog()
        self.detection_characteristic()
        self.draw()

    def check_entered_data(self):
        if 80 < self.phase_grad < 100 or 260 < self.phase_grad < 280:
            self.phase = randint(0, 360) * np.pi / 180

    def cor(self):
        x = [0] * 55 + list(self.function.counts_with_noise[1]) + [0] * 10
        # s = self.counts[1]
        s = Cos().create_counts()[1]
        time = np.arange(self.function.start_piece - 55 * self.function.T,
                         self.function.end_piece + 11 * self.function.T, self.function.T)
        corr = []
        for j, t in enumerate(time):
            Xc = 0
            Xs = 0
            for i in range(len(s)):
                if i + j > len(x) - 1:
                    Xc += 0
                    Xs += 0
                else:
                    pfi = i * self.w * self.function.T
                    Xc += x[i + j] * np.cos(pfi) * s[i]
                    Xs += x[i + j] * np.sin(pfi) * s[i]
            corr.append(Xc ** 2 + Xs ** 2)
        self.corr = time, corr
        return self.corr

    def porog(self):
        self.count_gamma()
        self.gamma_level = self.gamma_2()
        hypothesis = []
        for i, x in enumerate(self.corr[1]):
            if x > self.gamma_level:
                hypothesis.append(1)
            else:
                hypothesis.append(0)
        self.hypothesis = self.corr[0], hypothesis
        return self.hypothesis

    def gamma_2(self):
        x = np.exp((self.function.Energy / (4 * self.function.sigma ** 2)))
        i = 0
        min = float(besseli(0, i, derivative=0))
        while x > min:
            i += 0.001
            min = float(besseli(0, i, derivative=0))
        self.gamma_level = (i * self.function.sigma ** 2 * self.gamma) ** 2
        return (i * self.sigma ** 2 * self.gamma) ** 2

    def draw(self):
        Draw(func=self.function.analog[1], time=self.function.analog[0],
             title=f"Исходный сигнал c неизвестной начальной фазой",
             xlabel="t [мс]", ylabel="V [мВ]",
             name=self.function.name, flabel=f"Начальная фаза {int(self.phase_grad)} градусов",
             main_dir_name="Оптимальный обнаружитель при некогерентном приеме").draw()

        Draw(func=self.function.analog_with_noise[1], time=self.function.analog_with_noise[0],
             title=f"Воздействие помехи на {self.function.name}",
             name=self.function.name, main_dir_name="Оптимальный обнаружитель при некогерентном приеме",
             flabel=f"Фаза {int(self.phase_grad)} градусов", ).draw()

        Draw(func=self.corr[1], time=self.corr[0],
             title=f"После коррелятора {self.function.name}",
             name=self.function.name, main_dir_name="Оптимальный обнаружитель при некогерентном приеме",
             flabel=f"Фаза {int(self.phase_grad)} градусов", ).draw()

        Draw(func=self.hypothesis[1], time=self.hypothesis[0],
             title=f"Принятие решения {self.function.name}",
             name=self.function.name, main_dir_name="Оптимальный обнаружитель при некогерентном приеме",
             flabel=f"Фаза {int(self.phase_grad)} градусов", ).draw()



    def detection_characteristic(self):
        ash = (self.function.A*10**-3)**2
        N = len(self.function.counts[1])
        a=0.02
        self.d = [x for x in np.arange(0.01, 1.14, 0.08)]
        sigma = [self.function.Energy/x**2 for x in self.d]
        print("Energy=", self.function.Energy)
        print("sigma=", sigma)
        print(ash)
        b = [(N*ash / (2 * s ** 2)) ** 0.5 for s in sigma]
        print(b)
        alfa = [np.exp(-self.gamma_level**2 / (s**2*self.function.Energy)) for s in sigma]
        y0 = (2*np.log(1/a))**0.5
