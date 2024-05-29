import pygame
from constant import *
from shape import *
from algorithm import *

class Snake_Part():
    def __init__(self, surface: pygame.Surface, position: tuple[int, int], direction: str, type: str, color: pygame.Color) -> None:
        self.direction = direction
        self.type = type
        self.shape = Rectangle(surface, position, PART_SIZE, PART_SIZE, fill_color = color)
        if self.type == 'head':
            self.shape.fill_color = SNAKE_HEAD_COLOR

    def draw(self) -> None:
        self.shape.fill()

    def move(self) -> None:
        if self.direction == 'none':
            return
        direction = DIRECTION_DICT[self.direction]
        self.shape.position = (self.shape.position[0] + direction[0] * PART_SIZE, self.shape.position[1] + direction[1] * PART_SIZE)
        self.shape.rect.x, self.shape.rect.y = self.shape.position

class Snake:
    def __init__(self, surface: pygame.Surface, id: tuple[int, int], food_id: tuple[int, int] = INIT_FOOD_ID,  noises: list[tuple[int, int]] = INIT_NOISES, is_player_2 = False) -> None:
        self.surface = surface
        self.id = id
        self.food_id = food_id
        self.noises = noises
        if not is_player_2:
            self.player_no = 1
            self.color = SNAKE1_COLOR
            self.keys = [pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP]
        else:
            self.player_no = 2
            self.color = SNAKE2_COLOR
            self.keys = [pygame.K_d, pygame.K_s, pygame.K_a, pygame.K_w]
        if self.id[0] < INIT_SNAKE_PARTS_NUM - 1:
            self.head_direction = 'left'
        else:
            self.head_direction = 'right'
        self.head_position = (BOARD_OFFSET + self.id[0] * CELL_SIZE + PART_SIZE, BOARD_OFFSET + self.id[1] * CELL_SIZE + PART_SIZE)
        self.parts: list[Snake_Part] = []
        self.position_direction_dict: dict[tuple[int, int], str] = {}
        self.advanced_direction = 'none'
        self.frame = 0
        self.is_eating = False
        self.eating_combo = 0
        self.length = INIT_SNAKE_PARTS_NUM
        self.generate_init_parts()
        self.algorithm = Algorithm(self.get_parts_id(), self.noises)

    def generate_init_parts(self) -> None:
        position = self.head_position
        for part_id in range((self.length - 2) * 3 + 4):
            if part_id == 0:
                part_type = 'head'
            elif part_id == ((self.length - 2) * 3 + 3):
                part_type = 'tail'
            else:
                part_type = 'body'
            self.parts.append(Snake_Part(self.surface, position, self.head_direction, part_type, self.color))
            direction = DIRECTION_DICT[self.head_direction]
            position = (position[0] - direction[0] * PART_SIZE, position[1] - direction[1] * PART_SIZE)

    def add_parts(self) -> None:
        tail = self.parts[-1]
        tail_direction = DIRECTION_DICT[self.parts[-1].direction]
        new_tail = Snake_Part(self.surface, (tail.shape.position[0] - tail_direction[0] * PART_SIZE, tail.shape.position[1] - tail_direction[1] * PART_SIZE), self.parts[-1].direction, 'tail', self.color)
        self.parts[-1].type = 'body'
        self.parts.append(new_tail)
        if self.frame == 2:
            self.eating_combo -= 1
        if self.eating_combo == 0:
            self.is_eating = False

    def get_parts_id(self) -> list[tuple[int, int]]:
        parts_id: list[tuple[int, int]] = []
        for part in self.parts:
            id = ((part.shape.position[0] - BOARD_OFFSET) // CELL_SIZE, (part.shape.position[1] - BOARD_OFFSET) // CELL_SIZE)
            if id not in parts_id:
                parts_id.append(id)
        return parts_id

    def draw(self) -> None:
        for part in self.parts:
            part.draw()

    def set_direction(self) -> None:
        if self.frame == 0 and self.advanced_direction != 'none':
            self.head_direction = self.advanced_direction
            self.position_direction_dict[self.head_position] = self.head_direction
            self.advanced_direction = 'none'
        for part in self.parts:
            part_position = part.shape.position
            if not part_position in self.position_direction_dict:
                continue
            part.direction = self.position_direction_dict[part_position]
            if part.type == 'head':
                self.head_direction = self.position_direction_dict[part_position]

    def move(self) -> None:
        for part in self.parts:
            part_position = part.shape.position
            part.move()
            if part.type == 'head':
                self.head_position = part.shape.position
                if self.is_eating:
                    self.add_parts()
            if part.type == 'tail' and part_position in self.position_direction_dict:
                self.position_direction_dict.pop(part_position)
        self.frame = (self.frame + 1) % 3

    def handle_keys(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[self.keys[0]] and self.head_direction != 'left':
            direction = 'right'
        elif keys[self.keys[1]] and self.head_direction != 'up':
            direction = 'down'
        elif keys[self.keys[2]] and self.head_direction != 'right':
            direction = 'left'
        elif keys[self.keys[3]] and self.head_direction != 'down':
            direction = 'up'
        else:
            return
        self.advanced_direction = direction
        
    def is_food_found(self, food_id: tuple[int, int]) -> bool:
        food_position = (BOARD_OFFSET + food_id[0] * CELL_SIZE + PART_SIZE, BOARD_OFFSET + food_id[1] * CELL_SIZE + PART_SIZE)
        if self.head_position == food_position:
            self.is_eating = True
            self.eating_combo += 1
            self.length += 1
            self.algorithm.is_found = False
            return True
        return False

    def is_dead(self, other_snake_parts: list[Snake_Part] = []) -> bool:
        # if snake touch a border
        if self.head_position[0] + PART_SIZE == BOARD_WIDTH + BOARD_OFFSET:
            return True
        if self.head_position[1] + PART_SIZE == BOARD_HEIGHT + BOARD_OFFSET:
            return True
        if self.head_position[0] == BOARD_OFFSET:
            return True
        if self.head_position[1] == BOARD_OFFSET:
            return True
        
        # if snake touch a self's part
        parts = self.parts[2:] + other_snake_parts
        for part in parts:
            if (self.head_position[0] + PART_SIZE, self.head_position[1]) == part.shape.position:
                return True
            if (self.head_position[0], self.head_position[1] + PART_SIZE) == part.shape.position:
                return True
            if (self.head_position[0] - PART_SIZE, self.head_position[1]) == part.shape.position:
                return True
            if (self.head_position[0], self.head_position[1] - PART_SIZE) == part.shape.position:
                return True
            
        # if snake touch a noise
        for noise in self.noises:
            noise_position = (noise[0] * CELL_SIZE + BOARD_OFFSET, noise[1] * CELL_SIZE + BOARD_OFFSET)
            if (self.head_position[0] + PART_SIZE, self.head_position[1]) == (noise_position[0], noise_position[1] + PART_SIZE):
                return True
            if (self.head_position[0], self.head_position[1] + PART_SIZE) == (noise_position[0] + PART_SIZE, noise_position[1]):
                return True
            if (self.head_position[0] - CELL_SIZE, self.head_position[1]) == (noise_position[0], noise_position[1] + PART_SIZE):
                return True
            if (self.head_position[0], self.head_position[1] - CELL_SIZE) == (noise_position[0] + PART_SIZE, noise_position[1]):
                return True
        return False
    
    def is_near_dead(self, other_snake_parts: list[Snake_Part]) -> bool:
        if self.frame != 0:
            return False
        for part in other_snake_parts:
            if self.head_direction == 'right' and (self.head_position[0] + CELL_SIZE, self.head_position[1]) == part.shape.position:
                return True
            if self.head_direction == 'down' and (self.head_position[0], self.head_position[1] + CELL_SIZE) == part.shape.position:
                return True
            if self.head_direction == 'left' and (self.head_position[0] - CELL_SIZE, self.head_position[1]) == part.shape.position:
                return True
            if self.head_direction == 'up' and (self.head_position[0], self.head_position[1] - CELL_SIZE) == part.shape.position:
                return True
        return False

    def find_path(self, algorithm_name: str, food_id: tuple[int, int], other_snake_parts: list[Snake_Part] = []) -> None:
        if self.frame != 0:
            return
        if self.algorithm.is_found:
            self.algorithm.is_found = False if self.is_near_dead(other_snake_parts) else True
        if algorithm_name == 'DFS' and self.algorithm.is_found:
            return
        other_snake_parts_id: list[tuple[int, int]] = []
        for part in other_snake_parts:
            id = ((part.shape.position[0] - BOARD_OFFSET) // CELL_SIZE, (part.shape.position[1] - BOARD_OFFSET) // CELL_SIZE)
            if id not in other_snake_parts_id:
                other_snake_parts_id.append(id)
        self.algorithm.input_current_state(self.get_parts_id(), other_snake_parts_id, food_id, algorithm_name)
        if algorithm_name == 'DFS':
            self.algorithm.dfs()
        elif algorithm_name == 'BFS':
            self.algorithm.bfs()
        elif algorithm_name == 'UCS':
            self.algorithm.ucs()
        elif algorithm_name == 'Greedy':
            self.algorithm.greedy()
        elif algorithm_name == 'A Star':
            self.algorithm.a_star()
        if not self.algorithm.is_found:
            return
        for position in self.algorithm.path:
            self.position_direction_dict[position[0]] = position[1]