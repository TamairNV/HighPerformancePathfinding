import pygame.draw
import CustomDataStructures as dataS
import math
import random
import threading




class Entity():
    pathNumber = 0
    speed = 7
    pathingObjects = []
    targets = []
    def __init__(self,location):
        self.pos = location
        self.grid = None
        self.realPos = (self.pos[0] * 14, self.pos[1] * 14)
        self.pathI = 0
        self.path = []
        self.completedPath = False
        self.targets = []
        self.thread = None
        self.lastTarget = None




    def Run(self,target,screen,baseGrid):
        #self.grid.resetGrid(self.grid, baseGrid)
        targetNode = self.grid.grid[target[0]][target[1]]
        targetNode.resetNode("t")


        self.pos = (int(self.realPos[0]//14),int(self.realPos[1]//14))
        start = self.grid.grid[self.pos[0]][self.pos[1]]
        start.resetNode("s")


        pQueue = dataS.PriorityQueue()
        pQueue.push(start)
        targetNode.pathID +=1
        start.pathID +=1

        try:
            while not pQueue.pop().expandParent(self.grid.grid,targetNode,pQueue,baseGrid):
                pass
        except:
            self.grid.resetGrid(self.grid, baseGrid)
            print("error")
            self.Run(target,screen,baseGrid)
            return


        #self.drawPath(targetNode.path,screen)
        targetNode.path.reverse()
        self.path = targetNode.path
        self.followPath()

    def followPath(self):
        self.completedPath = False
        if self not in Entity.pathingObjects:
            Entity.pathingObjects.append(self)



    def stepPath(self,screen,baseGrid,draw = False):
        if draw:
            self.drawGrid(screen)
        if not self.completedPath:
            if math.fabs(self.realPos[0] - self.path[self.pathI].x*14 ) < 2 and math.fabs(self.realPos[1] - self.path[self.pathI].y*14 ) < 2:
                if self.pathI >= len(self.path)-1:
                    self.completedPath = True
                    self.thread = threading.Thread(target=self.runInThread, args=(screen, baseGrid))
                    self.thread.start()
                    self.pathI = 0
                    return True
                self.pathI +=1


            dir = self.getDir(self.realPos,(self.path[self.pathI].x*14,self.path[self.pathI].y*14),Entity.speed)

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
                    pygame.draw.rect(screen,(255,255,0),(x*14,y*14,14,14))
                if self.grid.grid[x][y].state == "p":
                    pygame.draw.rect(screen,(255,10,255),(x*14,y*14,14,14))


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
            pygame.draw.line(screen,self.generateColor(Entity.pathNumber),(path[i].x*14+7,path[i].y*14+7),(path[i+1].x*14+7,path[i+1].y*14+7),3)

        pygame.display.flip()

    def generateColor(self,counter):

        red = (counter * 123) % 256
        green = (counter * 231) % 256
        blue = (counter * 87) % 256
        return (red, green, blue)








