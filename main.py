from Draw import Draw

print("Start import")
from Cos import Cos
from Noise import Noise
from Rectangle import Rectangle
from Triangle import Triangle

print("Start import")

from Optimal_Detector import Optimal_Detector

from Correlation_Detector import Correlation_Detector

print("=" * 100)
print("\t\tИдет загрузка!")
print("=" * 100)

n = 2
if n == 1:
    Correlation_Detector(function=Cos, start_piece=0, t_start=2, t_end=4, end_piece=6).study()
    #Correlation_Detector(function=Triangle, start_piece=0, t_start=2, t_end=4, end_piece=6).study()
    #Correlation_Detector(function=Rectangle, start_piece=0, t_start=2, t_end=4, end_piece=6).study()
    #Noise().show_noise()
if n == 2:
    Optimal_Detector().run()
