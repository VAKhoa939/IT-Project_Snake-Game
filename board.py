import pygame, numpy as np
from constants import *
from events import *
from rectangle import *
BLACK = pygame.Color(0,0,0)

class Cell(Rectangle):
    def __init__(self, surface, position, id):
        super().__init__(surface, position, CELL_SIZE, CELL_SIZE, CELL_LINE_COLOR)
        self.id = id
        self.offset = CELL_SIZE // 3
        self.value = 0

    def draw_object(self, direction = 'none'):
        pygame.draw.rect(self.surface, GREEN, pygame.Rect(self.position[0] + self.offset, self.position[1] + self.offset, self.offset, self.offset))
        if direction == 'r':
            pygame.draw.rect(self.surface, GREEN, pygame.Rect(self.position[0] + 2 * self.offset, self.position[1] + self.offset, self.offset, self.offset))
        if direction == 'd':
            pygame.draw.rect(self.surface, GREEN, pygame.Rect(self.position[0] + self.offset, self.position[1] + 2 * self.offset, self.offset, self.offset))
        if direction == 'l':
            pygame.draw.rect(self.surface, GREEN, pygame.Rect(self.position[0], self.position[1] + self.offset, self.offset, self.offset))
        if direction == 'u':
            pygame.draw.rect(self.surface, GREEN, pygame.Rect(self.position[0] + self.offset, self.position[1], self.offset, self.offset))

    def get_neighbors(self, rows, columns):
        neighbors = []
        if self.id[0] + 1 < columns: #right
            neighbors.append([self.id[0] + 1, self.id[1]])
        if self.id[1] + 1 < rows: #down
            neighbors.append([self.id[0], self.id[1] + 1])
        if self.id[0] - 1 > -1: #left
            neighbors.append([self.id[0] - 1, self.id[1]])
        if self.id[1] - 1 > -1: #up
            neighbors.append([self.id[0], self.id[1] - 1])
        return neighbors

class Board(Rectangle):
    def __init__(self, surface):
        super().__init__(surface, [BOARD_OFFSET // 2, BOARD_OFFSET // 2], BOARD_WIDTH - BOARD_OFFSET, BOARD_HEIGHT - BOARD_OFFSET, BORDER_COLOR, BOARD_COLOR)
        self.cells = []
        self.values = np.zeros((ROWS, COLUMNS), dtype='uint8')
        for i in range(COLUMNS):
            column_cells = []
            for j in range(ROWS):
                cell = Cell(self.surface, [self.position[0] + CELL_SIZE * i, self.position[1] + CELL_SIZE * j], [i, j])
                column_cells.append(cell)
            self.cells.append(column_cells)

    def draw(self):
        self.board = pygame.draw.rect(self.surface, BOARD_COLOR, pygame.Rect(self.position[0], self.position[1], self.width, self.height))
        for column_cells in self.cells:
            for cell in column_cells:
                cell.draw_border()
                if not (cell.value == 0):
                    cell.draw_object()
                    neighbors = cell.get_neighbors(ROWS, COLUMNS)
                    self.connect_neighbors(cell.id, neighbors)
        self.draw_border()
        # print(self.values)

    def is_clicked(self, event, mouse, value = 1):
        if is_clicked(self, event, mouse):
            cell_id = [(mouse[0] - self.position[0]) // CELL_SIZE, (mouse[1] - self.position[1]) // CELL_SIZE]
            if self.cells[cell_id[0]][cell_id[1]].value == 1:
                self.cells[cell_id[0]][cell_id[1]].value = 0
                self.values[cell_id[0]][cell_id[1]] = 0
            else:
                self.cells[cell_id[0]][cell_id[1]].value = 1
                self.values[cell_id[0]][cell_id[1]] = 1
            return 1
        return 0

    def connect_neighbors(self, cell_id, neighbors):
        for position in neighbors:
            if not (self.cells[cell_id[0]][cell_id[1]].value == self.cells[position[0]][position[1]].value):
                continue
            if position[0] > cell_id[0]: #right
                self.cells[cell_id[0]][cell_id[1]].draw_object('r')
                self.cells[position[0]][position[1]].draw_object('l')
            if position[1] > cell_id[1]: #down
                self.cells[cell_id[0]][cell_id[1]].draw_object('d')
                self.cells[position[0]][position[1]].draw_object('u')
            if position[0] < cell_id[0]: #left
                self.cells[cell_id[0]][cell_id[1]].draw_object('l')
                self.cells[position[0]][position[1]].draw_object('r')
            if position[1] < cell_id[1]: #up
                self.cells[cell_id[0]][cell_id[1]].draw_object('u')
                self.cells[position[0]][position[1]].draw_object('d')
