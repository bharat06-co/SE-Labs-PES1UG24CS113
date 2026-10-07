import pygame


class Snake:
    def __init__(self, x, y, cell_size):
        self.cell_size = cell_size
        # body is a list of (x, y) grid-cell positions, head is body[0]
        self.body = [(x, y), (x - 1, y), (x - 2, y)]
        self.direction = (1, 0)  # direction of the last actual move
        self.turn_queue = []
        self.max_turn_queue = 2
        self.grow_pending = False

    def set_direction(self, dx, dy):
        new_direction = (dx, dy)

        # Compare against the last actual move when the queue is empty,
        # otherwise compare against the last queued turn. This prevents
        # rapid key presses from eventually creating a 180-degree turn.
        reference_direction = self.turn_queue[-1] if self.turn_queue else self.direction

        # Ignore duplicate directions and direct reversals.
        if new_direction == reference_direction:
            return
        if new_direction == (-reference_direction[0], -reference_direction[1]):
            return

        if len(self.turn_queue) < self.max_turn_queue:
            self.turn_queue.append(new_direction)

    def move(self):
        # Apply the next queued turn immediately before this actual move.
        if self.turn_queue:
            self.direction = self.turn_queue.pop(0)

        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)
        if self.grow_pending:
            self.grow_pending = False
        else:
            # Remove the tail before self-collision is checked. This means
            # moving into the cell the tail is leaving is allowed.
            self.body.pop()

    def grow(self):
        self.grow_pending = True

    def head_rect(self):
        x, y = self.body[0]
        return pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

    def segment_rects(self):
        return [
            pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
            for (x, y) in self.body
        ]

    def collides_with_self(self):
        head = self.body[0]
        return head in self.body[1:]

    def collides_with_wall(self, grid_width, grid_height):
        x, y = self.body[0]
        return x < 0 or y < 0 or x >= grid_width or y >= grid_height
