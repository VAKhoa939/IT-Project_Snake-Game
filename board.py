import pygame, random, numpy as np
from constant import *
from shape import *
from snake import *

class Board(Rectangle):
    def __init__(self, surface: pygame.Surface) -> None:
        super().__init__(surface, (BOARD_OFFSET, BOARD_OFFSET), BOARD_WIDTH, BOARD_HEIGHT, fill_color = BOARD_COLOR)
        self.cells: dict[tuple[int, int], Cell] = {}
        self.init_values = np.zeros((ROWS, COLUMNS), dtype = 'uint8')
        for i in range(COLUMNS):
            for j in range(ROWS):
                self.cells[i, j] = Cell(self.surface, (self.position[0] + CELL_SIZE * i, self.position[1] + CELL_SIZE * j), (i, j))
        self.food_id = INIT_FOOD_ID
        self.noises: list[tuple[int, int]] = INIT_NOISES
        
        self.snake1_id = INIT_SNAKE1_ID
        self.snake1 = Snake(self.surface, INIT_SNAKE1_ID)
        self.cells[self.snake1_id].value = self.init_values[self.snake1_id[1]][self.snake1_id[0]] = OBJECT_DICT['snake1']
        
        self.snake2_id = INIT_SNAKE2_ID
        self.snake2 = Snake(self.surface, INIT_SNAKE2_ID, is_player_2 = True)
        self.cells[self.snake2_id].value = self.init_values[self.snake2_id[1]][self.snake2_id[0]] = OBJECT_DICT['snake2']

        self.cells[self.food_id].value = self.init_values[self.food_id[1]][self.food_id[0]] = OBJECT_DICT['food']

        self.is_two_player = True
        self.allow_show_path = True
        self.is_mouse_hold = False

    def draw(self) -> None:
        self.board = pygame.draw.rect(self.surface, BOARD_COLOR, pygame.Rect(self.position[0], self.position[1], self.width, self.height))
        if not self.is_two_player and self.allow_show_path:
            if self.snake1.algorithm.is_found:
                self.draw_path()
        self.snake1.draw()
        if self.is_two_player:
            self.snake2.draw()
        for cell_id in self.cells:
            self.cells[cell_id].draw_border()
            self.cells[cell_id].draw_object()
        self.draw_border()

    def draw_path(self) -> None:
        frontier_id: list[tuple[int, int]] = [frontier_node.id for frontier_node in self.snake1.algorithm.frontier]
        visited_id: list[tuple[int, int]] = [visited_key for visited_key in self.snake1.algorithm.visited]

        path_id: list[tuple[int, int]] = [part_id for part_id in self.snake1.algorithm.snake_parts_id]
        for position in self.snake1.algorithm.path:
            id = ((position[0][0] - BOARD_OFFSET) // CELL_SIZE, (position[0][1] - BOARD_OFFSET) // CELL_SIZE)
            path_id.append(id)
        path_id.append(self.food_id)

        for id in frontier_id:
            self.cells[id].draw_path(OBJECT_DICT['frontier'])
        for id in visited_id:
            self.cells[id].draw_path(OBJECT_DICT['visited'])
        for id in path_id:
            self.cells[id].draw_path(OBJECT_DICT['path'])

    def text_to_value(self, text: str) -> int:
        for i in range(len(OBJECT_NAMES)):
            if OBJECT_NAMES[i] != text:
                continue
            if i == 0:
                return OBJECT_DICT['empty']
            elif i == 1:
                return OBJECT_DICT['snake1']
            elif i == 2:
                return OBJECT_DICT['snake2']
            elif i == 3:
                return OBJECT_DICT['food']
            elif i == 4:
                return OBJECT_DICT['noise']
        return OBJECT_DICT['empty']

    def is_released(self, event: pygame.event.Event, mouse: tuple[int, int]) -> bool:
        if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(mouse[0], mouse[1]):
            return True
        return False

    def is_editing(self, event: pygame.event.Event, mouse: tuple[int, int], text: str) -> bool:
        if self.is_clicked(event, mouse):
            self.is_mouse_hold = True
        if self.is_released(event, mouse):
            self.is_mouse_hold = False
        if not self.is_mouse_hold:
            return False
        value = self.text_to_value(text)
        cell_id: tuple[int, int] = ((mouse[0] - BOARD_OFFSET) // CELL_SIZE, (mouse[1] - BOARD_OFFSET) // CELL_SIZE)
        if not self.cells[cell_id].value == value and self.is_id_valid(cell_id, value):
            self.change_value(cell_id, value)
        return True

    def change_value(self, cell_id: tuple[int, int], value: int):
        if value == OBJECT_DICT['empty']:
            self.noises.remove(cell_id)
        
        elif value == OBJECT_DICT['snake1']:
            self.cells[self.snake1_id].value = OBJECT_DICT['empty']
            self.snake1_id = cell_id
        
        elif value == OBJECT_DICT['snake2']:
            self.cells[self.snake2_id].value = OBJECT_DICT['empty']
            self.snake2_id = cell_id
        
        elif value == OBJECT_DICT['food']:
            self.cells[self.food_id].value = OBJECT_DICT['empty']
            self.food_id = self.snake1.food_id = self.snake2.food_id = cell_id
        
        elif value == OBJECT_DICT['noise']:
            self.noises.append(cell_id)

        self.cells[cell_id].value = value
        self.snake1 = Snake(self.surface, self.snake1_id, self.food_id, self.noises)
        self.snake2 = Snake(self.surface, self.snake2_id, self.food_id, self.noises, is_player_2 = True)

    def is_id_valid(self, id, value) -> bool:
        if value == OBJECT_DICT['snake1'] or value == OBJECT_DICT['snake2']:
            new_snake = Snake(self.surface, id)
            snake_parts_id = new_snake.get_parts_id()
            for part_id in snake_parts_id:
                if self.cells[part_id].value != value and self.cells[part_id].value != OBJECT_DICT['empty']:
                    return False
        else:
            snake_parts_id = self.snake1.get_parts_id() + self.snake2.get_parts_id()
            for part_id in snake_parts_id:
                if id == part_id:
                    return False
            if value == OBJECT_DICT['empty']:
                return False if self.cells[id].value == OBJECT_DICT['food'] else True
            if self.cells[id].value != OBJECT_DICT['empty']:
                return False
        return True

    def respawn_food(self) -> None:
        old_food_id = self.food_id
        while self.is_id_valid(self.food_id, OBJECT_DICT['food']) == False:
            self.food_id = (random.randrange(0, COLUMNS), random.randrange(0, ROWS))
        self.cells[old_food_id].value = OBJECT_DICT['empty']
        self.cells[self.food_id].value = OBJECT_DICT['food']
        self.snake1.food_id = self.food_id
        self.snake2.food_id = self.food_id
                
    def reset(self) -> None:
        self.noises.clear()
        for i in range(COLUMNS):
            for j in range(ROWS):
                self.cells[i, j].value = self.init_values[j][i]
                if self.cells[i, j].value == OBJECT_DICT['snake1']:
                    self.snake1_id = (i, j)
                if self.cells[i, j].value == OBJECT_DICT['snake2']:
                    self.snake2_id = (i, j)
                if self.cells[i, j].value == OBJECT_DICT['food']:
                    self.food_id = (i, j)
                if self.cells[i, j].value == OBJECT_DICT['noise']:
                    self.noises.append((i, j))
        self.snake1 = Snake(self.surface, self.snake1_id, self.food_id)
        self.snake2 = Snake(self.surface, self.snake2_id, self.food_id, is_player_2 = True)

    def save(self) -> None:
        self.init_values = np.zeros((ROWS, COLUMNS), dtype = 'uint8')
        self.init_values[self.snake1_id[1]][self.snake1_id[0]] = OBJECT_DICT['snake1']
        self.init_values[self.snake2_id[1]][self.snake2_id[0]] = OBJECT_DICT['snake2']
        self.init_values[self.food_id[1]][self.food_id[0]] = OBJECT_DICT['food']
        for noise in self.noises:
            self.init_values[noise[1]][noise[0]] = OBJECT_DICT['noise']

class Cell(Rectangle):
    def __init__(self, surface: pygame.Surface, position: tuple[int, int], id: tuple[int, int], value = OBJECT_DICT['empty']) -> None:
        super().__init__(surface, position, CELL_SIZE, CELL_SIZE, border_color = CELL_LINE_COLOR)
        self.id = id
        self.value = value

    def draw_object(self) -> None:
        if self.value == OBJECT_DICT['food']:
            pygame.draw.rect(self.surface, FOOD_COLOR, pygame.Rect(self.position[0] + PART_SIZE, self.position[1] + PART_SIZE, PART_SIZE, PART_SIZE))
        elif self.value == OBJECT_DICT['noise']:
            pygame.draw.rect(self.surface, NOISE_COLOR, pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

    def draw_path(self, value: int) -> None:
        if value == OBJECT_DICT['frontier']:
            pygame.draw.rect(self.surface, FRONTIER_COLOR, pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))
        elif value == OBJECT_DICT['visited']:
            pygame.draw.rect(self.surface, VISITED_COLOR, pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))
        elif value == OBJECT_DICT['path']:
            pygame.draw.rect(self.surface, PATH_COLOR, pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))