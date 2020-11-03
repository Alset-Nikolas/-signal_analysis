import numpy as np
import matplotlib.pyplot as plt
from Signal import Signal


class Rectangle(Signal):
    def __init__(self, sigma=0.001):
        super().__init__(name="Прямоугольный импульс")
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
        counts = []
        time = np.arange(self.start_piece, self.end_piece + self.T, self.T)
        for t in time:
            self.M += 1
            if self.t_start <= t <= self.t_start + self.tau:
                counts.append(self.A)
                self.Energy += round(self.A ** 2, 2)
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
        counts = []
        time = np.arange(self.start_piece, self.end_piece + self.T, self.T / 100)
        for t in time:
            if self.t_start <= t <= self.t_start + self.tau:
                counts.append(self.A)
            else:
                counts.append(0)
        if counts == [0] * len(counts):
            self.fd *= 2
            self.create_counts()
        self.analog = [time, counts]
        return time, counts


if __name__ == "__main__":
    cos = Rectangle().study()

    plt.show()
