import numpy as np
from Signal import Signal


class Cos(Signal):
    """ Создает обьект косинус"""

    def __init__(self, phase=0, sigma=0.001):
        super().__init__(name="Гармонический сигнал", phase=phase)
        self.sigma = sigma

    def create_signal(self):
        self.create_counts()
        self.create_analog()
        self.add_noise(sigma=self.sigma)

    def create_analog(self):
        """
                    Создадим аналоговый сигнал
                    :return t, s(t) = A*cos(2*pi*f*t)
        """
        time = np.arange(self.start_piece, self.end_piece + self.T, self.T / 100)
        analog_cos = []
        for t in time:
            if self.t_start <= t <= self.t_start + self.tau:
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
        time = np.arange(self.start_piece, self.end_piece + self.T, self.T)
        for t in time:
            self.M += 1
            if self.t_start <= t <= self.t_start + self.tau:
                pfi = 2 * np.pi * self.fs * t + self.phase
                counts.append(round(self.A * np.cos(pfi), 2))
                self.Energy += round((self.A * np.cos(pfi)) ** 2, 2)
            else:
                counts.append(0)
        if counts == [0] * len(counts):
            self.fd *= 2
            self.create_counts()
        print(f"===================={self.Energy}===============")
        self.Energy /= 10 ** 6  # тк мВ*мв
        self.counts = [time, counts]
        return time, counts
