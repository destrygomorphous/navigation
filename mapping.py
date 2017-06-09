#!/usr/bin/env python

import random
import numpy as np
import matplotlib.pyplot as plt

class OGrid:
    def __init__(self):
        self.oGrid = None
        self.roboStartx = 0
        self.roboStarty = 0

    def getVal(self, x, y):
        return self.oGrid[y, x]

    def setOGrid(self, grid):
        self.oGrid = grid.astype(np.float16)

class NavigatorRandom:
    def __init__(self):
        # 0=obstacle, 1=free, .5=unknown
        self.oGrid = None
        self.viewRadius = 1

    def initOGrid(self, amap):
        self.oGrid = np.empty_like(amap.oGrid)
        self.oGrid.fill(0.5)

    def getMove(self, x, y):
        # 0 is up, 1 is up right, 2 is right, etc.
        # return 2
        return random.randint(0, 7)

    def updateOGrid(self, x, y, val):
        self.oGrid[y, x] = val

    def showOGrid(self):
        plt.imshow(self.oGrid, interpolation='none')
        plt.show()

def updateRoboGrid(nav, amap, x, y):
    h, w = amap.oGrid.shape
    if nav.viewRadius == 1:
        for j in [y - 1, y, y + 1]:
            if j >= 0 and j < h:
                for i in [x - 1, x, x + 1]:
                    if i >= 0 and i < w:
                        nav.updateOGrid(i, j, amap.getVal(i, j))

def explore(nav, amap, iterations):
    x = amap.roboStartx
    y = amap.roboStarty
    h, w = amap.oGrid.shape
    # List of positions for plotting later
    xPosns = [0] * iterations
    yPosns = [0] * iterations
    for iter in range(iterations):
        xPosns[iter] = x
        yPosns[iter] = y
        updateRoboGrid(nav, amap, x, y)
        move = nav.getMove(x, y)
        if (move == 0) and (y - 1 >= 0) and (amap.oGrid[y - 1, x] == 1):
            y -= 1
        elif (move == 1) and (y - 1 >= 0) and (x + 1 < w) and (amap.oGrid[y - 1, x + 1] == 1):
            y -= 1
            x += 1
        elif (move == 2) and (x + 1 < w) and (amap.oGrid[y, x + 1] == 1):
            x += 1
        elif (move == 3) and (y + 1 < h) and (x + 1 < w) and (amap.oGrid[y + 1, x + 1] == 1):
            y += 1
            x += 1
        if (move == 4) and (y + 1 < h) and (amap.oGrid[y + 1, x] == 1):
            y += 1
        elif (move == 5) and (y + 1 < h) and (x - 1 >= 0) and (amap.oGrid[y + 1, x - 1] == 1):
            y += 1
            x -= 1
        elif (move == 6) and (x - 1 >= 0) and (amap.oGrid[y, x - 1] == 1):
            x -= 1
        elif (move == 7) and (y - 1 >= 0) and (x - 1 >= 0) and (amap.oGrid[y - 1, x - 1] == 1):
            y -= 1
            x -= 1
    implot = plt.imshow(nav.oGrid, interpolation='none', cmap='gray', vmin=0, vmax=1)
    plt.plot(xPosns, yPosns, c='r')
    plt.xlim(0, w - 1)
    plt.ylim(0, h - 1)
    plt.show()

if __name__ == '__main__':
    mapa = OGrid()
    arr = np.full((16, 16), 1)
    arr[0, :] = 0
    arr[-1, :] = 0
    arr[:, 0] = 0
    arr[:, -1] = 0
    arr[2:4, 2:4] = 0
    mapa.setOGrid(arr)
    mapa.roboStartx = 8
    mapa.roboStarty = 8
    magellan = NavigatorRandom()
    magellan.initOGrid(mapa)
    explore(magellan, mapa, 300)
