import math
import pygame


class node:
    def __init__(self, pos, state):
        self.parent = None
        self.f_cost = 0
        self.g_cost = 0
        self.h_cost = 0
        self.pos = pos
        self.state = state
        self.path = []
        self.pathID = 0

    def resetNode(self, state):
        self.parent = None
        self.f_cost = 0
        self.g_cost = 0
        self.h_cost = 0
        if state == "w":
            self.state = state
        else:
            self.state = ""
        self.path = []

    def __lt__(self, other):
        return self.f_cost < other.f_cost

    def TraceBack(self):
        currentNode = self

        while currentNode != None:
            self.path.append(currentNode)
            currentNode.state = "l"
            currentNode = currentNode.parent

    def minDistance(self, other):
        dx = abs(self.pos[0] - other.pos[0])
        dy = abs(self.pos[1] - other.pos[1])
        return math.sqrt(dx ** 2 + dy ** 2)

    def calF_cost(self):
        self.f_cost = self.g_cost + self.h_cost

    def expandParent(self, grid, endnode, visitedNodes, baseGrid):

        if self == endnode:
            self.TraceBack()
            return True
        if self.pathID != endnode.pathID:
            self.pathID = endnode.pathID
            self.resetNode(baseGrid[self.pos[0]][self.pos[1]])

        self.state = "p"
        for i in range(self.pos[0] - 1, self.pos[0] + 2):
            for j in range(self.pos[1] - 1, self.pos[1] + 2):
                if (i >= 0 and i < len(grid)) and (j >= 0 and j < len(grid[0])):

                    if grid[i][j].pathID != endnode.pathID or grid[i][j].state == "l":
                        grid[i][j].pathID = endnode.pathID
                        grid[i][j].resetNode(baseGrid[i][j])

                    if grid[i][j] != self and grid[i][j].state not in  ("d","p","w"):
                        grid[i][j].parent = self
                        grid[i][j].g_cost = self.g_cost + grid[i][j].minDistance(self)
                        grid[i][j].h_cost = grid[i][j].minDistance(endnode)
                        grid[i][j].calF_cost()
                        grid[i][j].state = "d"
                        visitedNodes.push(grid[i][j])
                    elif grid[i][j].state == "d" and grid[i][j].parent.g_cost >= self.g_cost:
                        grid[i][j].parent = self
                        grid[i][j].g_cost = self.g_cost + grid[i][j].minDistance(self)
                        grid[i][j].calF_cost()



        return False
