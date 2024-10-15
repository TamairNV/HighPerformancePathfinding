import pygame
import PathingObject
import UI
import CustomDataStructures as dataS
import pygameInput
import Painter
import Grid
import time
import json
pygame.init()


class Screen:

    def __init__(self, height, width, name):

        self.height = height
        self.width = width
        self.name = name
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        dataS.Transform.camera = self
        self.events = pygame.event.get()
        pygameInput.Input.startListening()
        self.position = dataS.Vector2(0, 0)
        self.frameRate = 1200
SCREEN = Screen(750,1000,"Pathfinding")
pygameInput.Input.screen = SCREEN
class Time:

    clock = pygame.time.Clock()
    deltaTime = 0

    @staticmethod
    def tick(frameRateCap):
        Time.deltaTime = Time.clock.tick(frameRateCap) / 1000.0  # Convert milliseconds to seconds


def CreateSidePannel():
    pass

AStarRunning = False

def Run():#34
    n = time.time()
    for target in Painter.Brush.targetsMade:
        for person in Painter.Brush.people:
            person.grid.resetGrid(person.grid,grid)

        for person in Painter.Brush.people:
            person.Run(target, SCREEN.screen)
    print(time.time()-n)

def drawGrid(grid):
    for row in range(len(grid[0])):
        for col in range(len(grid[1])):
            nearestX = round(row * 14)
            nearestY = round(col * 14)

            if grid[row][col].state == "p":
                pygame.draw.rect(SCREEN.screen, (255,0,0),(nearestX, nearestY, 14, 14))
            if grid[row][col].state == "d":
                pygame.draw.rect(SCREEN.screen, (255,255,0),(nearestX, nearestY, 14, 14))


Painter.Paint.SCREEN= SCREEN
grid = Painter.createGrid(SCREEN,(700,840),14)
def Save():
    with open("two.json", 'w') as file:
        json.dump(grid, file)


def Load(grid):
    with open("two.json", 'r') as file:
        loaded_grid = json.load(file)

    grid.clear()
    grid.extend(loaded_grid)

    for x in range(len(grid)):
        for y in range(len(grid[x])):

            if grid[x][y] == "people":
                Painter.Brush.peopleMade.append((x, y))
                person = PathingObject.Entity((x, y))
                Painter.Brush.entities[(x, y)] = person
                Painter.Brush.people.append(person)
                person.grid = Grid.Grid(Painter.Brush.grid)

            elif grid[x][y] == "target":
                Painter.Brush.targetsMade.append((x, y))
            elif grid[x][y] == "wall":
                Painter.Brush.wallsMade.append((x, y))

running = True
startButton = UI.Button(SCREEN, (900, 0), (100, 100), "Start", (200, 200, 200),Run)
saveButton = UI.Button(SCREEN, (900, 100), (100, 100), "Save", (200, 200, 200),Save)
loadButton = UI.Button(SCREEN, (900, 200), (100, 100), "load", (200, 200, 200),Load,arg=grid)

Painter.pallet()
SCREEN.screen.fill((255, 255, 255))


Painter.Brush.grid = grid
brush = Painter.Brush(SCREEN,(700,840),14,grid)
Painter.Paint.brush = brush
while running:
    Time.tick(SCREEN.frameRate)
    if len(Painter.Brush.people) == 0:
        SCREEN.screen.fill((255, 255, 255))
        Painter.createGrid(SCREEN, (700, 840), 14)
    SCREEN.events = pygame.event.get()
    pygameInput.keysPressed = pygame.key.get_pressed()
    brush.draw()
    brush.displayPoints()
    Painter.Paint.update()
    for event in SCREEN.events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()


    UI.Element.updateAllElements()

    pygameInput.Input.keysPressedLastFrame = pygame.key.get_pressed()
    pygame.display.flip()






