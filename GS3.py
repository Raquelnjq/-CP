import numpy as np
import pylab as plt
import os
import matplotlib.pyplot as plt
from scipy import asarray as ar
from scipy.optimize import curve_fit
import sys
import threading
import time

current_dir = os.path.abspath(os.path.dirname(__file__))
print(current_dir)
sys.path.append(current_dir)
x = ar(range(10))
y = ar([235, 431, 559, 723, 1256, 1433, 1024, 560, 478, 404])  # 词频


def gaussian(x, *param):
    return param[0] * np.exp(-np.power(x - param[2], 2.) / (2 * np.power(param[4], 2.))) + \
           param[1] * np.exp(-np.power(x - param[3], 2.) / (2 * np.power(param[5], 2.)))


popt, pcov = curve_fit(gaussian, x, y, p0=[3, 4, 3, 6, 1, 1])
print(popt)
print(pcov)

plt.plot(x, y, 'b+:', label='词频')
plt.plot(x, gaussian(x, *popt), 'ro:', label='词')
plt.legend()
plt.show()
