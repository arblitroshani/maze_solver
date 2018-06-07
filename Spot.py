import pygame
import random
from math import sqrt


class Spot(pygame.sprite.Sprite):

    def __init__(self, i, j, width, height, rows, cols):
        super(Spot, self).__init__()
        self.rect = pygame.Rect(i * width, j * height, width - 2, height - 2)
        self.BLUE = (0, 0, 255)
        self.i = i
        self.j = j
        self.f = 0
        self.g = 0
        self.h = 0
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.neighbors = []
        self.previous = None
        self.wall = False

        if random.random() < 0.3:
            self.wall = True

    def show(self, screen, col):
        if self.i == 0 and self.j == 0:
            col = (0, 255, 0)
        if self.i == self.rows - 1 and self.j == self.cols - 1:
            col = (255, 0, 0)
        if self.wall:
            col = (0, 0, 0)
        pygame.draw.rect(screen, col,
                         (self.i * self.width + 1,
                          self.j * self.height + 1,
                          self.width - 2,
                          self.height - 2))

    def add_neighbors(self, grid, allow_diag):
        i = self.i
        j = self.j

        if i < self.cols - 1:
            self.neighbors.append(grid[i + 1][j])
        if i > 0:
            self.neighbors.append(grid[i - 1][j])
        if j < self.rows - 1:
            self.neighbors.append(grid[i][j + 1])
        if j > 0:
            self.neighbors.append(grid[i][j - 1])
        if allow_diag:
            if i > 0 and j > 0:
                self.neighbors.append(grid[i - 1][j - 1])
            if i < self.cols - 1 and j > 0:
                self.neighbors.append(grid[i + 1][j - 1])
            if i > 0 and j < self.rows - 1:
                self.neighbors.append(grid[i - 1][j + 1])
            if i < self.cols - 1 and j < self.rows - 1:
                self.neighbors.append(grid[i + 1][j + 1])

    @staticmethod
    def heuristic(spot1, spot2):
        d = sqrt((spot1.i - spot2.i)**2 + (spot1.j - spot2.j)**2)
        return d
