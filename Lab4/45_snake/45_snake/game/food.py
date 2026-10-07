import pygame
import random


class Food:
    def __init__(self, grid_width, grid_height, cell_size, occupied_cells=None):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size
        self.x = None
        self.y = None
        self.respawn(occupied_cells if occupied_cells is not None else [])

    def respawn(self, occupied_cells):
        occupied = set(occupied_cells)
        free_cells = [
            (x, y)
            for y in range(self.grid_height)
            for x in range(self.grid_width)
            if (x, y) not in occupied
        ]

        if not free_cells:
            # The board is full; leave food absent rather than crashing.
            self.x = None
            self.y = None
            return

        self.x, self.y = random.choice(free_cells)

    def rect(self):
        if self.x is None or self.y is None:
            return pygame.Rect(0, 0, 0, 0)
        return pygame.Rect(self.x * self.cell_size, self.y * self.cell_size, self.cell_size, self.cell_size)
