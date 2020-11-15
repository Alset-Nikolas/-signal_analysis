import os

import numpy as np
import math
import matplotlib.pyplot as plt

from Draw import Draw


class Noise:
    def __init__(self, function=[], sigma=0.01):
        self.m = 0
        self.sigma = sigma
        self.N = len(function)
        self.noise = self.sigma * np.random.randn(self.N) + self.m
        self.function = function[:]
        self.E_noise = sum(self.noise ** 2)

    def add_noise(self):
        for i in range(self.N):
            self.function[i] += self.noise[i]

        return self.function

    def print_data_noise(self):
        text = f'''
==============================================================
=========================ШУМ==================================
==============================================================
        MO = {self.m} [В]
        sigma = {self.sigma} [кГц]

        Мощность сигнала P = {self.E_noise} [Вт]
==============================================================
==============================================================
==============================================================
        '''
        print(text)

    def show_noise(self):

        if self.N == 0:
            self.N = 100000
            self.sigma = 0.01
            self.m = 0

        s = self.sigma * np.random.randn(self.N) + self.m
        fig, ax = plt.subplots()
        count, bins, ignored = plt.hist(s, 100, density=True, label=f'Гистограмма: N(кол-во эл-ов) = {self.N}')

        plt.plot(bins, 1 / (self.sigma * np.sqrt(2 * np.pi)) *
                 np.exp(- (bins - self.m) ** 2 / (2 * self.sigma ** 2)), linewidth=3, color='y'
                 , label="Теория: Нормальный закон распределения")
        plt.title(f"Плотность вероятности шума. sigma={self.sigma}")
        plt.legend()
        ax.grid()
        Draw().file_creation()
        name_save = 'Плотность вероятности шума.png'
        dir_name = "Photo"
        my_path = os.path.join(os.path.abspath(os.curdir), dir_name)
        fig.savefig(os.path.join(my_path, name_save))


if __name__ == "__main__":

    Noise(sigma=0.1).show_noise()
    plt.show()