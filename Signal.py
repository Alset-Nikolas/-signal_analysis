from Noise import Noise

class Signal:
    def __init__(self, name, phase=0):
        self.name = name
        self.A = 1
        self.fs = 1  # кГц
        self.phase = phase
        self.f = 4
        self.fd = self.f * 2  # кГц
        self.T = 1 / self.fd
        self.tau = 2.0  # мс

        self.t_start = 2  # мс
        self.t_end = self.t_start + self.tau

        self.start_piece = 0
        self.end_piece = self.t_start + 2 * self.tau

        self.Energy = 0
        self.M = 0
        self.counts = [None, None]  # [время соотве-ее к отсчетам, отсчеты по Td]
        self.analog = [None, None]

        self.analog_with_noise = [None, None]
        self.counts_with_noise = [None, None]

    def add_noise(self, sigma):
        analog_real = [x/1000 for x in self.analog[1]]
        f_noise = Noise(function=analog_real, sigma=sigma).add_noise()
        f_noise = [x * 1000 for x in f_noise]
        self.analog_with_noise = self.analog[0], f_noise
        self.counts_with_noise = self.analog[0][::100], f_noise[::100]
        return self.analog_with_noise, self.counts_with_noise

    def check_entered_data(self):
        """
                Проверяем входные данные
        """
        if self.fd < 2 * self.fs:
            print("Частота дискретизации fd > 2*f")
            return False
        if self.fd % 2 != 0:
            print("Частота дискретизации - четное число")
            return False
        if self.t_start < self.start_piece:
            print("t_start - время с которого начинается cos")
            print("start_piece - время с которого начинается сигнал")
            return False
        if self.end_piece < self.t_start + self.tau:
            print("end_piece >= self.t_start + self.tau")
            return False
        return True

    def show_pictures(self):
        """
                Рисуем графики
        """
        self.function.print_data()
        self.draw()

    def print_data(self):
        text = f'''
    ===============================================================================
    ========================={self.name}==================================
    ===============================================================================
            А = {self.A} [мВ]
            f = {self.fs} [кГц]
            1/f = {1 / self.fs} [мс]
            fd = {self.fd} [kГц]
            1/fd = {self.T} [мс]
            Длительность импулсьа tau = {self.tau} (c {self.t_start} до {self.t_start + self.tau}) [мс]

            Мощность сигнала P = {self.Energy} [Вт]
            sigma = {self.sigma}
            osh = {(self.Energy/self.sigma**2)**0.5}
    ===============================================================================
    ===============================================================================
    ===============================================================================
            '''
        print(text)
