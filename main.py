import matplotlib.pyplot as plt
from Cos import Cos
from Rectangle import Rectangle
from Triangle import Triangle

from Optimal_Detector import Optimal_Detector
from Correlation_Detector import Correlation_Detector

print("=" * 100)
print("\t\tИдет загрузка!")
print("=" * 100)

#Correlation_Detector(function=Cos).study()
Correlation_Detector(function=Triangle).study()
Correlation_Detector(function=Rectangle).study()
#Optimal_Detector().study()
plt.show()
