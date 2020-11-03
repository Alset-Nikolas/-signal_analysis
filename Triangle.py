import numpy as np
import matplotlib.pyplot as plt
from Signal import Signal


class Triangle(Signal):
    def __init__(self, sigma=0.001028205891675227):
        super().__init__(name="Треугольный импульс")
        self.sigma = sigma

    def create_signal(self):
        self.create_counts()
        self.create_analog()
        self.add_noise(sigma=self.sigma)

    def create_counts(self):
        """
            Создадим Прямоугольный импульс
            :return массив времени и отсчетов прямоугольного импульса
        """
        time = np.arange(self.start_piece, self.end_piece + self.T, self.T)
        counts = []
        t_center = (2 * self.t_start +
                    self.tau) // 2
        for t in time:
            self.M += 1
            if self.t_start <= t <= t_center:
                k = self.A / (t_center - self.t_start)
                b = -k * self.t_start
                counts.append(k * t + b)
                self.Energy += (k * t + b) ** 2
            elif t_center < t < self.t_end:
                k = self.A / (t_center - (self.t_start + self.tau))
                b = -k * (self.t_start + self.tau)
                counts.append(k * t + b)
                self.Energy += (k * t + b) ** 2
            else:
                counts.append(0)

        if counts == [0] * len(counts):
            self.fd *= 2
            self.create_counts()
        self.counts = [time, counts]
        self.Energy /= 10 ** 6  # тк мВ*мв
        return time, counts

    def create_analog(self):
        """
                    Создадим аналоговый сигнал
        """
        time = np.arange(self.start_piece, self.end_piece + self.T, self.T / 100)
        counts = []
        t_center = (2 * self.t_start +
                    self.tau) // 2
        for t in time:
            if self.t_start <= t <= t_center:
                k = self.A / (t_center - self.t_start)
                b = -k * self.t_start
                counts.append(k * t + b)
            elif t_center < t < self.t_start + self.tau:
                k = self.A / (t_center - (self.t_start + self.tau))
                b = -k * (self.t_start + self.tau)
                counts.append(k * t + b)
            else:
                counts.append(0)
        self.analog = [time, counts]
        return time, counts


if __name__ == "__main__":
    cos = Triangle().study()

    plt.show()
