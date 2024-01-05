import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from mpl_toolkits.mplot3d import Axes3D


path = r'C:\Users\Administrator\Desktop\allstation.txt'
path_left = r'C:\Users\Administrator\Desktop\left.txt'
path_right = r'C:\Users\Administrator\Desktop\right.txt'
data_left = np.loadtxt(path_left)
data_right = np.loadtxt(path_right)
target_left = data_left[:-2, :]
target_right = data_right[:-2, :]


def coordinate_transformation1(x, y):
    x = np.mat(x)
    y = np.mat(y)
    center_x = np.mean(x, axis=0)
    center_y = np.mean(y, axis=0)
    re_x = x - center_x
    re_y = y - center_y
    h = re_x.T*re_y
    u, s, vt = np.linalg.svd(h)
    r = vt.T*u.T
    if np.linalg.det(r) < 0:
        vt[2, :] *= -1
        r = vt.T*u.T
    t = -r*center_x.T + center_y.T
    return r, t


def coordinate_transformation2(x, y):
    x = np.mat(x)
    y = np.mat(y)
    center_x = np.mean(x, axis=0)
    center_y = np.mean(y, axis=0)
    re_x = x - center_x
    re_y = y - center_y
    r = np.linalg.inv(re_x.T*re_x)*re_x.T*re_y
    t = -r*center_x.T + center_y.T
    return r, t


r1, t1 = coordinate_transformation1(target_left, target_right)
r2, t2 = coordinate_transformation2(target_left, target_right)
result1 = np.mat(target_left)*r1 + t1.T
result2 = np.mat(target_left)*r2 + t2.T
# print(target_right)
# print(result1)
# print(result2)
print(11111)

