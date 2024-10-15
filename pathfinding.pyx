import math
import pygame
from typing import List, Optional

# Constants
DIAGDIST = 2 ** 0.5

cdef class Node:
    cdef int x
    cdef int y
    cdef Node parent  # Node type, may be None
    cdef float f_cost
    cdef float g_cost
    cdef float h_cost
    cdef tuple pos
    cdef str state
    cdef List[Node] path

    def __init__(self, pos: tuple[int, int], state: str):
        self.x = pos[0]
        self.y = pos[1]
        self.parent = None
        self.f_cost = 0.0
        self.g_cost = 0.0
        self.h_cost = 0.0
        self.pos = pos
        self.state = state
        self.path = []

    def reset_node(self, state: str):
        self.parent = None
        self.f_cost = 0.0
        self.g_cost = 0.0
        self.h_cost = 0.0
        self.state = state

    def __lt__(self, Node other) -> bool:
        return self.f_cost < other.f_cost

    def trace_back(self):
        cdef Node current_node = self
        while current_node is not None:
            self.path.append(current_node)
            current_node.state = "l"
            current_node = current_node.parent

    cdef float min_distance(self, Node other) -> float:
        cdef int dx = abs(self.x - other.x)
        cdef int dy = abs(self.y - other.y)
        return math.sqrt(dx ** 2 + dy ** 2)

    cdef void calculate_f_cost(self):
        self.f_cost = self.g_cost + self.h_cost

    cdef bool expand_parent(self, List[List[Node]] grid, Node end_node, visited_nodes):
        if self == end_node:
            self.trace_back()
            return True

        self.state = "p"
        cdef int i, j
        for i in range(max(0, self.x - 1), min(len(grid), self.x + 2)):
            for j in range(max(0, self.y - 1), min(len(grid[0]), self.y + 2)):
                Node neighbor_node = grid[i][j]

                if neighbor_node != self and (neighbor_node.state == "" or neighbor_node.state == "t"):
                    neighbor_node.parent = self
                    neighbor_node.g_cost = self.g_cost + neighbor_node.min_distance(self)
                    neighbor_node.h_cost = neighbor_node.min_distance(end_node)
                    neighbor_node.calculate_f_cost()
                    neighbor_node.state = "d"
                    visited_nodes.push(neighbor_node)
                elif neighbor_node.state == "d" and neighbor_node.parent.g_cost >= self.g_cost:
                    neighbor_node.parent = self
                    neighbor_node.g_cost = self.g_cost + neighbor_node.min_distance(self)
                    neighbor_node.calculate_f_cost()

        return False
