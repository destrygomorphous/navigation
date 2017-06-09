#!/usr/bin/env python

import random
import numpy as np
import matplotlib.pyplot as plt
import heapq
from Queue import Queue

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
        return random.randint(0, 7)

    def updateOGrid(self, x, y, val):
        self.oGrid[y, x] = val

    def showOGrid(self):
        plt.imshow(self.oGrid, interpolation='none')
        plt.show()

class NavigatorCurious(NavigatorRandom):
    def getMove(self, x, y):
        if self.oGrid[y + 1, x + 1] == 0.5:
            return 3
        if self.oGrid[y + 1, x - 1] == 0.5:
            return 5
        if self.oGrid[y - 1, x - 1] == 0.5:
            return 7
        if self.oGrid[y - 1, x + 1] == 0.5:
            return 1
        if self.oGrid[y - 1, x] == 0.5:
            return 0
        if self.oGrid[y + 1, x] == 0.5:
            return 4
        if self.oGrid[y, x + 1] == 0.5:
            return 2
        if self.oGrid[y, x - 1] == 0.5:
            return 6
        return random.randint(0, 7)

class NavigatorStraight(NavigatorRandom):
    def __init__(self, randomness): # 0.3 seems pretty good for randomness
        # 0=obstacle, 1=free, .5=unknown
        self.oGrid = None
        self.viewRadius = 1
        self.direction = 0
        self.randomness = randomness
    def getMove(self, x, y):
        if random.random() < self.randomness:
            self.direction = random.randint(0, 3) * 2
        while True:
            if self.direction == 0:
                if self.oGrid[y - 1, x] != 0:
                    return 0
                else:
                    self.direction = 2
            if self.direction == 2:
                if self.oGrid[y, x + 1] != 0:
                    return 2
                else:
                    self.direction = 4
            if self.direction == 4:
                if self.oGrid[y + 1, x] != 0:
                    return 4
                else:
                    self.direction = 6
            if self.direction == 6:
                if self.oGrid[y, x - 1] != 0:
                    return 6
                else:
                    self.direction = 0

class NavigatorBFS(NavigatorRandom):
    def __init__(self):
        # 0=obstacle, 1=free, .5=unknown
        self.oGrid = None
        self.viewRadius = 1
        self.directionQ = Queue()
    def getMove(self, x, y):
        if not self.directionQ.empty():
            return self.directionQ.get()
        h, w = self.oGrid.shape
        openI = Queue()
        closedI = set()
        path = []
        openI.put((x, y))
        while not openI.empty():
            cx, cy = openI.get()
            while (cx, cy) in closedI:
                if openI.empty():
                    return 0
                cx, cy = openI.get()
            path.append((cx, cy))
            closedI.add((cx, cy))
            for i in [cx - 1, cx, cx + 1]:
                for j in [cy - 1, cy, cy + 1]:
                    if (i, j) in closedI:
                        continue
                    if not (i >= 0 and i < w and j >= 0 and j < h) or self.oGrid[j, i] == 0:
                        continue
                    if self.oGrid[j, i] == 0.5:
                        print path
                        # dirs = directionsFromPath(path)
                        print x, y, i, j
                        dirs = AStar(self.oGrid, x, y, cx, cy)
                        print dirs
                        for dire in dirs:
                           self.directionQ.put(dire)
                        return self.directionQ.get()
                    openI.put((i, j))
            del path[-1]
        return 0


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
    print fractionExplored(nav.oGrid)
    implot = plt.imshow(nav.oGrid, interpolation='none', cmap='gray', vmin=0, vmax=1)
    plt.scatter([xPosns[0]], [yPosns[0]], s=80)
    plt.plot(xPosns, yPosns, c='r')
    plt.xlim(0, w - 1)
    plt.ylim(0, h - 1)
    plt.axis('off')
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
    # magellan = NavigatorRandom()
    # magellan = NavigatorCurious()
    # magellan = NavigatorStraight(randomness=0.3)
    magellan = NavigatorBFS()
    magellan.initOGrid(mapa)
    explore(magellan, mapa, 160)
