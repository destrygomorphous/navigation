#!/usr/bin/env python

import random
import numpy as np
import matplotlib.pyplot as plt
import heapq
from Queue import Queue
from navigators import *
from maps import *
from collections import Counter

class OGrid:
    def __init__(self):
        self.oGrid = None
        self.roboStartx = 0
        self.roboStarty = 0

    def getVal(self, x, y):
        return self.oGrid[y, x]

    def setOGrid(self, grid):
        self.oGrid = grid.astype(np.float16)

def dist(x0, y0, x1, y1):
    return ((x0 - x1) ** 2 + (y0 - y1) ** 2) ** 0.5

def directionsFromPath(path):
    directions = []
    c = path[0]
    for n in path[1:]:
        if n[1] - c[1] == -1 and n[0] == c[0]:
            directions.append(0)
        elif n[1] - c[1] == -1 and n[0] - c[0] == 1:
            directions.append(1)
        elif n[1] == c[1] and n[0] - c[0] == 1:
            directions.append(2)
        elif n[1] - c[1] == 1 and n[0] - c[0] == 1:
            directions.append(3)
        elif n[1] - c[1] == 1 and n[0] == c[0]:
            directions.append(4)
        elif n[1] - c[1] == 1 and n[0] - c[0] == -1:
            directions.append(5)
        elif n[1] == c[1] and n[0] - c[0] == -1:
            directions.append(6)
        elif n[1] - c[1] == -1 and n[0] - c[0] == -1:
            directions.append(7)
        else:
            print "fuck"
        c = n
    return directions

def reconstructPath(cameFrom, c):
    totalPath = [c]
    while c in cameFrom.keys():
        c = cameFrom[c]
        totalPath.append(c)
    # print totalPath
    directions = directionsFromPath(list(reversed(totalPath)))
    # print directions
    return directions

# sx and sy are the start coordinates, ex and ey the end
# Returns a list of directions to take
def AStar(oGrid, sx, sy, ex, ey):
    h, w = oGrid.shape
    closedSet = set()
    openSet = set()
    openSet.add((sx, sy))
    cameFrom = {}
    gScore = {}
    gScore[(sx, sy)] = 0
    fScore = []
    heapq.heappush(fScore, (dist(sx, sy, ex, ey), (sx, sy)))
    while openSet: # while not empty
        cx, cy = heapq.heappop(fScore)[1]
        if (cx, cy) == (ex, ey):
            return reconstructPath(cameFrom, (cx, cy))
        openSet.remove((cx, cy))
        closedSet.add((cx, cy))
        for i in [cx - 1, cx, cx + 1]:
            for j in [cy - 1, cy, cy + 1]:
                if (i, j) in closedSet:
                    continue
                if not (i >= 0 and i < w and j >= 0 and j < h and oGrid[j, i] == 1):
                    continue
                if (i, j) not in openSet:
                    openSet.add((i, j))
                tentativegScore = gScore[(cx, cy)] + 1
                if tentativegScore >= gScore.get((i, j), float('inf')):
                    continue
                cameFrom[(i, j)] = (cx, cy)
                gScore[(i, j)] = tentativegScore
                heapq.heappush(fScore, (tentativegScore + dist(i, j, ex, ey), (i, j)))
    print "Failure"
    return False

def testAStar():
    oGrid = np.ones((3,3))
    AStar(oGrid, 0, 0, 2, 2)
    oGrid[1,1] = 0
    AStar(oGrid, 0, 0, 2, 2)

def updateRoboGrid(nav, amap, x, y):
    h, w = amap.oGrid.shape
    if nav.viewRadius == 1:
        for j in [y - 1, y, y + 1]:
            if j >= 0 and j < h:
                for i in [x - 1, x, x + 1]:
                    if i >= 0 and i < w:
                        nav.updateOGrid(i, j, amap.getVal(i, j))

def fractionExplored(oGrid):
    unique, counts = np.unique(oGrid, return_counts=True)
    d = dict(zip(unique, counts))
    return 1 - d.get(0.5, 0) / float(oGrid.size)

def fractionRepeated(xlist, ylist):
    d = Counter(zip(xlist, ylist))
    return (len(xlist) - len(d.keys())) / float(len(xlist))

def explore(nav, amap, iterations):
    x = amap.roboStartx
    y = amap.roboStarty
    h, w = amap.oGrid.shape
    # List of positions for plotting later
    xPosns = [0] * iterations
    yPosns = [0] * iterations
    explored = [0] * iterations
    repeats = [0] * iterations
    for iter in range(iterations):
        xPosns[iter] = x
        yPosns[iter] = y
        explored[iter] = fractionExplored(nav.oGrid)
        repeats[iter] = fractionRepeated(xPosns[:iter + 1], yPosns[:iter + 1])
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
    print fractionExplored(nav.oGrid)
    implot = plt.imshow(nav.oGrid, interpolation='none', cmap='gray', vmin=0, vmax=1)
    plt.scatter([xPosns[0]], [yPosns[0]], s=80)
    plt.plot(xPosns, yPosns, c='r')
    plt.xlim(0, w - 1)
    plt.ylim(0, h - 1)
    plt.axis('off')
    plt.show()
    return (repeats, explored)

if __name__ == '__main__':
    mapa = OGrid()
    mapa.setOGrid(bigMap())
    mapa.roboStartx = 59
    mapa.roboStarty = 59

    # magellan0 = NavigatorRandom()
    # magellan1 = NavigatorCurious()
    # magellan2 = NavigatorStraight(randomness=0.3)
    # magellan3 = NavigatorBFS()
    # magellan0.initOGrid(mapa)
    # magellan1.initOGrid(mapa)
    # magellan2.initOGrid(mapa)
    # magellan3.initOGrid(mapa)
    # repeats0, explored0 = explore(magellan0, mapa, 2000)
    # repeats1, explored1 = explore(magellan1, mapa, 2000)
    # repeats2, explored2 = explore(magellan2, mapa, 2000)
    # repeats3, explored3 = explore(magellan3, mapa, 2000)
    # fig, ax = plt.subplots()
    # plt.plot(repeats0, explored0, label='Random Navigator')
    # plt.plot(repeats1, explored1, label='Curious Navigator')
    # plt.plot(repeats2, explored2, label='Straight Navigator')
    # plt.plot(repeats3, explored3, label='BFS Navigator')
    # plt.xlabel('Fraction repeated positions')
    # plt.ylabel('Fraction map explored')
    # plt.ylim(0, 1)
    # plt.xlim(-0.01, .6)
    # plt.title('Map explored vs repeated positions')
    # plt.legend()
    # plt.show()
    mapa.setOGrid(bigMap())
    h, w = mapa.oGrid.shape
    plt.imshow(mapa.oGrid, interpolation='none', cmap='gray', vmin=0, vmax=1)
    plt.xlim(0, w - 1)
    plt.ylim(0, h - 1)
    plt.axis('off')
    plt.show()
