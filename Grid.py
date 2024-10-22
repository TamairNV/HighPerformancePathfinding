

import AStar

class Grid:
    CELLSIZE = 7
    def __init__(self,baseGrid):
        self.grid = [[AStar.node((x,y),baseGrid[x][y]) for y in range(len(baseGrid[0]))] for x in range(len(baseGrid[1]))]



    def resetGrid(self,grid,baseGrid):
        [[grid.grid[x][y].resetNode(baseGrid[x][y]) for y in range(len(baseGrid[0]))] for x in range(len(baseGrid[1]))]


