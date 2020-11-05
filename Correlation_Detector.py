import os
import matplotlib.pyplot as plt
import numpy as np
from Draw import Draw
from scipy import special
from Signal import Signal
from scipy.stats import norm
from Cos import Cos
from Noise import Noise
from scipy.stats import norm


class Correlation_Detector(Signal):
    def __init__(self, function):
        self.function = function()
        self.function_obj = function
        self.corr = [None, None]

        self.alfa = 0.5
        self.gamma = None
        self.hypothesis = [None, None]

        self.a = [0.2, 0.02, 0.002]
        self.detection_characteristic_teory = None
        self.detection_characteristic_praktik = None
        self.d = None

        self.dir_name = "Photo"
        self.my_path = os.path.join(os.path.abspath(__file__), self.dir_name)

    def recovery_kotelnikov(self):
        """
                    Восстаановим сигнал по выборке
                    :return t, _s(t)
        """
        dt = self.T / 100
        time = np.arange(self.start_piece, self.end_piece + dt, dt)

        kotelnikov = [0] * len(time)

        for i, t in enumerate(time):

            if not self.t_start <= t <= self.t_start + self.tau:
                kotelnikov[i] = 0
            else:
                for j, x in enumerate(self.counts[1]):
                    pfi = 2 * np.pi * self.fs * (t - j * self.T)
                    if pfi == 0:
                        kotelnikov[i] += x
                    else:
                        kotelnikov[i] += x * np.sin(pfi) / pfi
                if kotelnikov[i] > self.A:
                    kotelnikov[i] = self.A
                if kotelnikov[i] < -self.A:
                    kotelnikov[i] = -self.A
        self.kotelnikov = time, kotelnikov

    def study(self):
        """Запуск"""

        self.function.create_signal()
        # self.recovery_kotelnikov()
        self.cor()
        self.porog()
        self.detection_characteristic()

        self.show_pictures()

    def draw(self):
        Draw(func=self.function.analog[1], time=self.function.analog[0],
             count_3=self.function.counts[1], t_count_3=self.function.counts[0],
             title=f"Исходный сигнал {self.function.name}",
             xlabel="t [мс]", ylabel="V [В]",
             name=self.function.name,
             main_dir_name="Корреляционный обнаружитель").draw()
        '''
        Draw(func=self.kotelnikov[1], time=self.kotelnikov[0],
             title=f"Восстановим {self.name} по Теореме Котельникова",
             xlabel="t [мс]", ylabel="V [В]", name=self.name,
             main_dir_name="Корреляционный обнаружитель").draw()
        '''
        Draw(func=self.function.analog_with_noise[1], time=self.function.analog_with_noise[0],
             count_3=self.function.counts_with_noise[1], t_count_3=self.function.counts_with_noise[0],
             title=f"Воздействие помехи на {self.function.name}",
             name=self.function.name, main_dir_name="Корреляционный обнаружитель",
             flabel=f"ОСШ = {round((self.function.Energy / self.function.sigma ** 2) ** 0.5,1)}").draw()
        Draw(self.corr[1], self.corr[0],
             func_2=[self.gamma*10**6]*len(self.corr[0]), time_2=self.corr[0],
             title=f'После коррелятора {self.function.name}',
             xlabel="смещение копии на tau [мс]", ylabel="V [мкВ]",
             name=self.function.name,
             main_dir_name="Корреляционный обнаружитель").draw()
        Draw(self.hypothesis[1], self.hypothesis[0],
             title=f'Принятие решения {self.function.name}',
             xlabel="смещение копии на tau [мс]",ylabel="Есть/Нету",
             name=self.function.name,
             main_dir_name="Корреляционный обнаружитель").draw()

        Draw(self.detection_characteristic_teory[0], self.d, flabel=f"Теория, вероятность ложной тревоги = {self.a[0]}",
             func_2=self.detection_characteristic_teory[1], time_2=self.d, flabel_2=f"Теория, влт = {self.a[1]}",
             func_3=self.detection_characteristic_teory[2], time_3=self.d, flabel_3=f"Теория, влт = {self.a[2]}",
             count=self.detection_characteristic_praktik[0], t_count=self.d, clabel="Эксперимент",
             count_2=self.detection_characteristic_praktik[1], t_count_2=self.d,
             count_3=self.detection_characteristic_praktik[2], t_count_3=self.d,
             title=f'Характеристика обнаружения {self.function.name}',
             xlabel="ОСШ", ylabel="Характеристика обнаружения",
             name=self.function.name,
             main_dir_name="Корреляционный обнаружитель").draw()

    def cor(self):
        x = [0] * 55 + [x/1000 for x in list(self.function.counts_with_noise[1])] + [0] * 10
        s = [x/1000 for x in self.function.counts[1]]
        time = np.arange(self.function.start_piece - 55 * self.function.T,
                         self.function.end_piece + 11 * self.function.T, self.function.T)
        corr = []
        for i, t in enumerate(time):
            sum = 0
            for j, si in enumerate(s):
                if j + i >= len(x):
                    sum += 0
                else:
                    sum += si * x[j + i]
            corr.append(sum)
        corr =[x*10**6 for x in corr]
        self.corr = time, corr

    def porog(self):
        self.gamma = self.count_gamma()
        hypothesis = []
        for x in self.corr[1]:
            x /=10**6
            if x >= self.gamma:
                hypothesis.append(1)
            else:
                hypothesis.append(0)
        self.hypothesis = self.corr[0], hypothesis

    def count_gamma(self):
        self.gamma = special.erfinv(self.alfa) * self.function.sigma * self.function.Energy ** 0.5
        return self.gamma

    def detection_characteristic(self):
        """
        Характеристика обнаружения
        :return:
        """
        self.d = [x for x in np.arange(0.01, 10, 1)]  # Отношение сигнал/шум
        sigma = [(self.function.Energy) ** 0.5 / x for x in self.d]
        self.detection_characteristic_teory = [[] for _ in range(len(self.a))]
        self.detection_characteristic_praktik = [[] for _ in range(len(self.a))]
        for q, a_ in enumerate(self.a):  # Для разных вероятностей ложной тревоги
            gamma = [(-1) * norm.ppf(a_) * (s ** 2 * self.function.Energy) ** 0.5 for s in sigma]  # Порог
            for j in range(len(gamma)):  # Теория
                x = 1 - norm.cdf((gamma[j] - self.function.Energy) / (sigma[j] * self.function.Energy ** 0.5))
                self.detection_characteristic_teory[q].append(x)

            for k, s in enumerate(sigma):  # Эксперимент
                f = self.function_obj(sigma=s)
                f.create_signal()
                m = 0
                N = 1000  # кол-во эксп-ов
                for i in range(N):
                    sk = [x / 1000 for x in f.counts[1]]  # Перевод в мВ
                    xk = Noise(function=sk, sigma=s).add_noise()  # Cигнал + шум с sigma=s
                    T = 0
                    for j in range(len(xk)):
                        T += sk[j] * xk[j]
                    y = gamma[k]
                    if T > y:
                        m += 1
                self.detection_characteristic_praktik[q].append(m / N)

