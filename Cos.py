import numpy as np

from Draw import Draw
from Signal import Signal


class Cos(Signal):
    """ Создает обьект косинус"""

    def __init__(self, t_start=2, sigma=0.001, **kwargs):
        super().__init__(name="Гармонический сигнал", **kwargs)
        self.sigma = sigma
        self.t_start = t_start

    def create_signal(self):
        self.create_counts()
        self.create_analog()
        self.add_noise(sigma=self.sigma)

    def create_analog(self):
        """
                    Создадим аналоговый сигнал
                    :return t, s(t) = A*cos(2*pi*f*t)
        """
        time = np.arange(self.start_piece, self.end_piece, self.T / 100)
        analog_cos = []
        for t in time:
            if self.t_start <= t <= self.t_end:
                pfi = 2 * np.pi * self.fs * t + self.phase
                analog_cos.append(round(self.A * np.cos(pfi), 5))
            else:
                analog_cos.append(0)

        self.analog = time, analog_cos
        return time, analog_cos

    def create_counts(self):
        """
                   Создадим выборку сигнала по fd
                   :return t[k], s(t[k])
        """
        counts = []
        time = np.arange(self.start_piece, self.end_piece, self.T)
        for t in time:
            self.M += 1
            if self.t_start <= t <= self.t_end:
                pfi = 2 * np.pi * self.fs * t + self.phase
                counts.append(round(self.A * np.cos(pfi), 2))
                self.Energy += round((self.A * np.cos(pfi)) ** 2, 2)
            else:
                counts.append(0)

        self.counts = [time, counts]
        return time, counts

    def show_cos(self):
        Draw(func=self.analog[1], time=self.analog[0],
             count_3=self.counts[1], t_count_3=self.counts[0],
             title=f"Исходный сигнал {self.name}",
             xlabel="t [мс]", ylabel="V [мВ]",
             main_dir_name="Корреляционный обнаружитель").draw()


