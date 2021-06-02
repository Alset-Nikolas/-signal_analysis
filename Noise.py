import os

import numpy as np
import math
import matplotlib.pyplot as plt

from Draw import Draw


class Noise:
    def __init__(self, sigma=0.7):
        self.m = 0
        self.sigma = sigma

    def add_noise(self, function):
        return [x+y for x, y in zip(function, self.sigma * np.random.randn(len(function)))]

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


        self.N = 100000
        self.sigma = 0.65
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