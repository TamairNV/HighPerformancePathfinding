import pygame.draw
import CustomDataStructures as dataS
class Entity():
    pathNumber = 0
    def __init__(self,location):
        self.pos = location
        self.grid = None

    def resetGrid(self):
        for x in range(len(self.grid.grid[0])):
            for y in range(len(self.grid.grid[1])):
                self.grid[x][y].resetNode()

    def Run(self,target,screen):
        target = self.grid.grid[target[0]][target[1]]
        target.state = "t"
        start = self.grid.grid[self.pos[0]][self.pos[1]]
        start.state = "s"

        pQueue = dataS.PriorityQueue()
        pQueue.push(start)
        while not pQueue.pop().expandParent(self.grid.grid,target,pQueue):
            pass
        self.drawPath(target.path,screen)


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









