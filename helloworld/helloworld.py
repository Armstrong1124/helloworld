import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from mpl_toolkits.mplot3d import Axes3D


path = r'C:\Users\Administrator\Desktop\allstation.txt'
path_left = r'C:\Users\Administrator\Desktop\left.txt'
path_right = r'C:\Users\Administrator\Desktop\right.txt'
data_left = np.mat(np.loadtxt(path_left))
target_left = np.insert(data_left[:6, :], 3, values=0, axis=1)
wheel_left = np.insert(data_left[6:, :], 3, values=0, axis=1)
data_right = np.mat(np.loadtxt(path_right))
target_right = np.insert(data_right[:6, :], 3, values=0, axis=1)
wheel_right = np.insert(data_right[6:, :], 3, values=0, axis=1)
print(data_left)
print(data_right)

