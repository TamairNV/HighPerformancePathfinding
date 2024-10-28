import pygame.draw
import CustomDataStructures as dataS
import math
import random
import threading
import time
import Cache
import Grid
import copy


class Entity():

    pathNumber = 0

    pathingObjects = []
    targets = []
    running = False
    totalPaths = 0
    cache = Cache.cache()
    pathsCached = 0
    pathsCollectedFromCache = 0
    reversePathsCollectedFromCache = 0
    CELLSIZE = Grid.Grid.CELLSIZE
    speed = CELLSIZE
    def __init__(self,location):
        self.pos = location
        self.grid = None
        self.realPos = (self.pos[0] * Entity.CELLSIZE, self.pos[1] * Entity.CELLSIZE)
        self.pathI = 0
        self.path = []
        self.completedPath = False
        self.targets = []
        self.thread = None
        self.lastTarget = None


    def Run(self,target,screen,baseGrid):
        Entity.running = True
        #self.grid.resetGrid(self.grid, baseGrid)
        targetNode = self.grid.grid[target[0]][target[1]]
        targetNode.resetNode("t")
        self.pos = (int(self.realPos[0] // Entity.CELLSIZE), int(self.realPos[1] // Entity.CELLSIZE))
        start = self.grid.grid[self.pos[0]][self.pos[1]]
        start.resetNode("s")

        pQueue = dataS.PriorityQueue()
        pQueue.push(start)
        targetNode.pathID = Entity.totalPaths
        start.pathID = targetNode.pathID




        while not pQueue.pop().expandParent(self.grid.grid,targetNode,pQueue,baseGrid):
            if len(pQueue.heap) == 0:
                print(targetNode.pos,start.pos)
                self.grid.resetGrid(self.grid, baseGrid)
                print("error")
                return

        #self.drawPath(targetNode.path,screen)
        targetNode.path.reverse()
        self.path = targetNode.path
        self.followPath()
        Entity.totalPaths +=1

    def followPath(self):
        self.completedPath = False
        if self not in Entity.pathingObjects:
            Entity.pathingObjects.append(self)



    def stepPath(self,screen,baseGrid,draw = False):
        if draw:
            self.drawGrid(screen)
        if not self.completedPath:
            if math.fabs(self.realPos[0] - self.path[self.pathI].pos[0]*Entity.CELLSIZE ) < 2 and math.fabs(self.realPos[1] - self.path[self.pathI].pos[1]*Entity.CELLSIZE ) < 2:
                if self.pathI >= len(self.path)-1:
                    self.completedPath = True

                    self.thread = threading.Thread(target=self.runInThread, args=(screen, baseGrid))
                    self.thread.start()
                    self.pathI = 0

                    return True
                self.pathI +=1


            dir = self.getDir(self.realPos,(self.path[self.pathI].pos[0]*Entity.CELLSIZE,self.path[self.pathI].pos[1]*Entity.CELLSIZE),Entity.speed)

            self.realPos = (self.realPos[0] + dir[0],self.realPos[1] + dir[1])

    def runInThread(self, screen, baseGrid):

        newTarget = Entity.targets[random.randint(0, len(Entity.targets) - 1)]
        while newTarget == self.lastTarget:
            newTarget = Entity.targets[random.randint(0, len(Entity.targets) - 1)]

        self.lastTarget = newTarget
        self.Run(newTarget, screen, baseGrid)

    def drawGrid(self,screen):
        for x in range(len(self.grid.grid[0])):
            for y in range(len(self.grid.grid[1])):
                if self.grid.grid[x][y].state == "d":
                    pygame.draw.rect(screen,self.generateColor(self.grid.grid[x][y].pathID),(x*Entity.CELLSIZE,y*Entity.CELLSIZE,Entity.CELLSIZE,Entity.CELLSIZE))
                if self.grid.grid[x][y].state == "p":
                    pygame.draw.rect(screen,self.generateColor(self.grid.grid[x][y].pathID),(x*Entity.CELLSIZE,y*Entity.CELLSIZE,Entity.CELLSIZE,Entity.CELLSIZE))
                if self.grid.grid[x][y].state == "l":
                    pygame.draw.rect(screen,self.generateColor(self.grid.grid[x][y].pathID),(x*Entity.CELLSIZE,y*Entity.CELLSIZE,Entity.CELLSIZE,Entity.CELLSIZE))


    def getDir(self, point1, point2,speed):
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]

        if dx != 0:
            dx = dx // abs(dx)
        if dy != 0:
            dy = dy // abs(dy)

        direction = (dx*speed, dy*speed)
        return direction

    def drawPath(self,path,screen):
        Entity.pathNumber+=1
        for i in range(len(path)-1):
            pygame.draw.line(screen,self.generateColor(Entity.pathNumber),(path[i].pos[0]*Entity.CELLSIZE+Entity.CELLSIZE/2,path[i].pos[1]*Entity.CELLSIZE+Entity.CELLSIZE/2),(path[i+1].pos[0]*Entity.CELLSIZE+Entity.CELLSIZE/2,path[i+1].pos[1]*Entity.CELLSIZE+Entity.CELLSIZE/2),3)

        pygame.display.flip()

    def generateColor(self,counter):

        red = (counter * 123) % 256
        green = (counter * 231) % 256
        blue = (counter * 87) % 256
        return (red, green, blue)








