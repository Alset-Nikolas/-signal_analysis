import matplotlib.pyplot as plt
import os


class Draw:
    def __init__(self, func=None, time=None,
                 func_2=None, time_2=None,
                 func_3=None, time_3=None,
                 count=None, t_count=None,
                 count_2=None, t_count_2=None,
                 count_3=None, t_count_3=None,
                 title=None,
                 xlabel="t [мс]", ylabel="V [мВ]",
                 flabel=None, flabel_2=None, flabel_3=None,
                 clabel = None,
                 name=None,
                 main_dir_name="Photo", ):
        self.name = name

        self.func = func
        self.func_2 = func_2
        self.func_3 = func_3
        self.time = time
        self.time_2 = time_2
        self.time_3 = time_3

        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

        self.clabel = clabel
        self.flabel = flabel
        self.flabel_2 = flabel_2
        self.flabel_3 = flabel_3

        self.count = count
        self.count_2 = count_2
        self.count_3 = count_3
        self.t_count = t_count
        self.t_count_2 = t_count_2
        self.t_count_3 = t_count_3

        self.main_dir_name = main_dir_name
        if self.name is None:
            self.dir_name = self.main_dir_name
        else:
            self.dir_name = os.path.join(self.main_dir_name, self.name)
        self.my_path = os.path.join(os.path.abspath(os.curdir), self.dir_name)

    def draw(self):
        self.file_creation()
        fig, ax = plt.subplots()

        if self.count is not None and self.t_count is not None:
            ax.scatter(self.t_count, self.count, c="blue", label=self.clabel)

        if self.count_2 is not None and self.t_count_2 is not None:
            ax.scatter(self.t_count_2, self.count_2, c="orange")
        if self.count_3 is not None and self.t_count_3 is not None:
            ax.scatter(self.t_count_3, self.count_3, c="red")


        if self.func is not None and self.time is not None:
            plt.plot(self.time, self.func, c="blue", label=self.flabel)
        if self.func_2 is not None and self.time_2 is not None:
            plt.plot(self.time_2, self.func_2, '-', c="orange",  label=self.flabel_2)
        if self.func_3 is not None and self.time_3 is not None:
            plt.plot(self.time_3, self.func_3, '-', c="red", label=self.flabel_3)

        if self.title:
            plt.title(self.title)
        if self.flabel or self.flabel_2 or self.flabel_3 or self.flabel:
            plt.legend()
        ax.grid()
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        name_save = self.title + '.png'
        fig.savefig(os.path.join(self.my_path, name_save))

    def file_creation(self):
        if not os.path.exists(self.main_dir_name):
            os.mkdir(self.main_dir_name)
            print(f"Папка {self.main_dir_name} создана")
        if not os.path.exists(self.dir_name):
            os.mkdir(self.dir_name)
            print(f"Файл {self.name} создан")
