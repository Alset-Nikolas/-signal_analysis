import numpy as np


class Noise:
    def __init__(self, function, sigma=0.01):
        self.m = 0
        self.sigma = sigma
        self.N = len(function)
        #self.noise = np.random.normal(self.m, self.sigma, self.N)
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
