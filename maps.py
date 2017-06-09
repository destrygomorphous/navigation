#!/usr/bin/env python

import numpy as np

# Map with one obstacle
def simpleMap():
    arr = np.full((16, 16), 1)
    arr[0, :] = 0
    arr[-1, :] = 0
    arr[:, 0] = 0
    arr[:, -1] = 0
    arr[2:4, 2:4] = 0
    return arr

# Map with donut
def donutMap():
    arr = np.full((16, 16), 1)
    arr[0, :] = 0
    arr[-1, :] = 0
    arr[:, 0] = 0
    arr[:, -1] = 0

    arr[6, 6:-6] = 0
    arr[-6, 6:-6] = 0
    arr[6:-6, 6] = 0
    arr[6:-6, -6] = 0
    return arr

# Slalom
def slalomMap():
    arr1 = np.full((32, 32), 1)
    arr1[0, :] = 0
    arr1[-1, :] = 0
    arr1[:, 0] = 0
    arr1[:, -1] = 0
    arr1[:-6, 8] = 0
    arr1[6:, 16] = 0
    arr1[:-6, 24] = 0
    return arr1
# Boxes
def boxMap():
    arr = np.full((32, 32), 1)
    arr[0, :] = 0
    arr[-1, :] = 0
    arr[:, 0] = 0
    arr[:, -1] = 0
    for i in range(4, 28, 6):
        for j in range(4, 28, 6):
            arr[i:i + 4, j : j + 4] = 0
    return arr

# The Big One
def bigMap():
    arr = np.full((128, 128), 1)
    arr[0, :] = 0
    arr[-1, :] = 0
    arr[:, 0] = 0
    arr[:, -1] = 0
    for i in range(10, 120, 20):
        for j in range(10, 120, 20):
            arr[i:i + 8, j : j + 8] = 0
    return arr
