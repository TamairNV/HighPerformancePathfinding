import pygame
import PathingObject
import UI
import CustomDataStructures as dataS
import pygameInput
import Painter
import Grid
import time
import json
import random
pygame.init()

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 30)
def drawFPSCounter(screen, clock):
    fps = int(clock.get_fps())  # Get FPS as an integer
    fps_text = font.render(f"FPS: {fps}", True, (255, 255, 255))  # Render FPS text
    screen.blit(fps_text, (10, 10))  # Draw FPS counter at the top-left corner

def drawPathsPerSecond(screen, pathsPerSecond):

    fps_text = font.render(f"PPS: {pathsPerSecond}", True, (255, 255, 255))  # Render FPS text
    screen.blit(fps_text, (10, 25))  # Draw FPS counter at the top-left corner

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


def CreateSidePannel():
    pass

AStarRunning = False

def Run():#34
    PathingObject.Entity.targets =Painter.Brush.targetsMade
    for person in Painter.Brush.people:
        person.Run(Painter.Brush.targetsMade[random.randint(0,len(Painter.Brush.targetsMade))-1],SCREEN.screen,grid)


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


import threading
import json


def loadPerson(x, y):
    person = PathingObject.Entity((x, y))
    Painter.Brush.entities[(x, y)] = person
    Painter.Brush.people.append(person)
    person.grid = Grid.Grid(Painter.Brush.grid)


def Load(grid):
    with open("two.json", 'r') as file:
        loaded_grid = json.load(file)

    grid.clear()
    grid.extend(loaded_grid)

    threads = []

    for x in range(len(grid)):
        for y in range(len(grid[x])):

            if grid[x][y] == "people":
                Painter.Brush.peopleMade.append((x, y))


                thread = threading.Thread(target=loadPerson, args=(x, y))
                threads.append(thread)
                thread.start()

            elif grid[x][y] == "target":
                Painter.Brush.targetsMade.append((x, y))
            elif grid[x][y] == "w":
                Painter.Brush.wallsMade.append((x, y))

    for thread in threads:
        thread.join()

    for person in Painter.Brush.people:
        person.grid.resetGrid(person.grid, Painter.Brush.grid)


running = True
startButton = UI.Button(SCREEN, (900, 0), (100, 100), "Start", (200, 200, 200),Run)
saveButton = UI.Button(SCREEN, (900, 100), (100, 100), "Save", (200, 200, 200),Save)
loadButton = UI.Button(SCREEN, (900, 200), (100, 100), "load", (200, 200, 200),Load,arg=grid)

Painter.pallet()
SCREEN.screen.fill((255, 255, 255))


Painter.Brush.grid = grid
brush = Painter.Brush(SCREEN,(700,840),14,grid)
Painter.Paint.brush = brush
timer = time.time()
totalTime = 0
pps  = 0
while running:

    clock.tick()
    SCREEN.screen.fill((200, 150, 200))
    #Painter.createGrid(SCREEN, (700, 840), 14)
    SCREEN.events = pygame.event.get()
    pygameInput.keysPressed = pygame.key.get_pressed()
    brush.draw()

    Painter.Paint.update()
    for event in SCREEN.events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()


    for i,objects in enumerate(PathingObject.Entity.pathingObjects):
        objects.stepPath(SCREEN.screen,grid)
        if i == 0 :
            objects.stepPath(SCREEN.screen, grid,draw = True)
        else:
            objects.stepPath(SCREEN.screen, grid)
        if pygame.mouse.get_pressed()[0]:
            if i ==0 :
                pos = pygame.mouse.get_pos()
                var = objects.grid.grid[round(pos[0] // 14)][round(pos[1] // 14)]
                print(var.state,var.pos)


    brush.displayPoints()

    UI.Element.updateAllElements()
    pygameInput.Input.keysPressedLastFrame = pygame.key.get_pressed()
    if totalTime == 0 and PathingObject.Entity.running:
        totalTime = time.time()
    if totalTime > 1:
        drawPathsPerSecond(SCREEN.screen, round(PathingObject.Entity.totalPaths / (time.time() - totalTime)))

    drawFPSCounter(SCREEN.screen, clock)
    pygame.display.flip()






