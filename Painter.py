


import pygame
import UI
import PathingObject
import Grid
class Paint():
    paints = []
    SCREEN = None
    brush = None
    typeColours = {'wall': (30, 30, 30), 'people': (30, 50, 200), 'target': (30, 200, 50)}

    def __init__(self,ID,colour,font = 16,shape = 1):
        Paint.paints.append(self)
        self.shape = shape
        self.ID = ID
        self.colour = colour
        self.button = None
        self.number = len(Paint.paints)-1

        self.font = font
        if self.shape == 1:
            self.button = UI.Button(Paint.SCREEN, (70*self.number + 5, 705), (40, 40), self.ID, self.colour,self.changeBrush)
        if self.shape == 2:
            self.button = UI.Button(Paint.SCREEN, (70*self.number + 5, 705), (40, 40), self.ID, self.colour,self.changeBrush,shape=2)
    def createButton(self):
        if self.shape == 1:
            pygame.draw.rect(Paint.SCREEN.screen, (40, 40, 40), (70*self.number, 700, 50, 50))
        if self.shape == 2:
            pygame.draw.circle(Paint.SCREEN.screen, (40, 40, 40), (70*self.number+25, 725 ), 25)
        self.button.font  =pygame.font.SysFont("Arial", self.font)
        self.button.fontColour = (255,255,255)

    def changeBrush(self):
        Paint.brush.currentBrush = self.ID

    @staticmethod
    def update():
        for paint in Paint.paints:
            paint.createButton()



class Brush():
    mouseRect = None
    peopleMade = []
    targetsMade = []
    wallsMade = []
    people = []
    entities = {}
    grid = None
    def __init__(self,SCREEN,gridSize,nodeSize,grid):
        self.currentBrush = None
        Brush.mouseRect = (pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], 4, 4)
        self.gridSize = gridSize
        self.nodeSize = nodeSize
        self.grid = grid
        self.SCREEN = SCREEN
        self.newWalls = True

    def draw(self):
        x,y = pygame.mouse.get_pos()
        nearestX = round((x - 7) / self.nodeSize)
        nearestY = round((y - 7) / self.nodeSize)
        if x >= 0 and x <= self.gridSize[1]-6 and y >= 0 and y <= self.gridSize[0]-6 and pygame.mouse.get_pressed()[0] and self.grid[nearestX][nearestY] == "":

            self.grid[nearestX][nearestY] = self.currentBrush
            if self.currentBrush == "people":
                Brush.peopleMade.append((nearestX, nearestY))
                person = PathingObject.Entity((nearestX, nearestY))
                Brush.entities[(nearestX, nearestY)] = person
                Brush.people.append(person)
                person.grid = Grid.Grid(Brush.grid)

            elif self.currentBrush == "target":
                Brush.targetsMade.append((nearestX, nearestY))
            elif self.currentBrush == "wall":
                Brush.wallsMade.append((nearestX, nearestY))
                self.newWalls = True

        if not pygame.mouse.get_pressed()[0] and self.newWalls:
            self.newWalls = False
            for person in Brush.people:
                person.grid.resetGrid(person.grid, Brush.grid)



    def displayPoints(self):

        for personLocation in Brush.people:
            pygame.draw.circle(self.SCREEN.screen,(30, 50, 200) ,
                               (personLocation.realPos[0] + self.nodeSize / 2, personLocation.realPos[1] + self.nodeSize / 2), self.nodeSize / 2)
        for targetLocation in Brush.targetsMade:
            pygame.draw.rect(self.SCREEN.screen, Paint.typeColours[self.grid[targetLocation[0]][targetLocation[1]]],
                             (targetLocation[0]*14, targetLocation[1]*14, self.nodeSize, self.nodeSize))
        self.drawWalls()
    def drawWalls(self):
        for wallLocation in Brush.wallsMade:
            pygame.draw.rect(self.SCREEN.screen, Paint.typeColours[self.grid[wallLocation[0]][wallLocation[1]]],
                             (wallLocation[0]*14, wallLocation[1]*14, self.nodeSize, self.nodeSize))


def createGrid(SCREEN,gridSize,nodeSize):
    grid = [["" for _ in range(gridSize[0])] for _ in range(gridSize[1])]
    for x in range(int(gridSize[1]/nodeSize+1)):
        pygame.draw.rect(SCREEN.screen,(0,0,0),(x*nodeSize,0,1,gridSize[0]))
    for y in range(int(gridSize[0]/nodeSize+1)):
        pygame.draw.rect(SCREEN.screen,(0,0,0), (0,y * nodeSize, gridSize[1], 1))

    return grid

def pallet():
    Paint("wall", (30,30,30))
    Paint("people", (30, 50, 200),font= 13,shape = 2)
    Paint("target", (30, 200, 50),font= 12)


