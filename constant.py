import pygame

CYAN = pygame.Color(176, 224, 230)
KHAKI = pygame.Color(240, 230, 140)
BLACK = pygame.Color(0, 0, 0)
GREEN =pygame.Color(0, 255, 0)
RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)
WHITE = pygame.Color(255, 255, 255)
GRAY = pygame.Color(128, 128, 128)
PINK = pygame.Color(255, 102, 178)
DARK_PINK = pygame.Color(204, 0, 102)
ORANGE = pygame.Color(255, 128, 0)
YELLOW = pygame.Color(255, 255, 0)
PURPLE = pygame.Color(128, 0, 255)

BACKGROUND_COLOR = BLUE
BOARD_COLOR = (50, 50, 50)
BORDER_COLOR = GREEN
CELL_LINE_COLOR = WHITE
BUTTON_COLOR = GREEN
COMBOBOX_COLOR = PINK
OPTION_COLOR = DARK_PINK
SNAKE1_COLOR = GREEN
SNAKE2_COLOR = ORANGE
SNAKE_HEAD_COLOR = WHITE
FOOD_COLOR = RED
NOISE_COLOR = GRAY
FRONTIER_COLOR = YELLOW
VISITED_COLOR = ORANGE
PATH_COLOR = CYAN
TEXT_COLOR = WHITE

TEXT_FONT = 'Consolas'
TEXT_SIZE = 25

FPS = 20

BOARD_WIDTH = 1200 # MAX = 1620
BOARD_HEIGHT = 600 # MAX = 920
BOARD_OFFSET = 50
CELL_SIZE = 60
PART_SIZE = CELL_SIZE // 3
COLUMNS = BOARD_WIDTH // CELL_SIZE
ROWS = BOARD_HEIGHT // CELL_SIZE
MODE_NAMES : list[str] = ['Manual', 'DFS', 'BFS', 'UCS', 'Greedy', 'A Star']
OBJECT_NAMES : list[str] = ['Empty', '1st Snake', '2nd Snake', 'Food', 'Noise']
OBJECT_DICT : dict[str, int] = {'empty' : 0, 'snake1' : 1, 'snake2' : 2, 'food' : 3, 'noise' : 4, 'frontier' : 5, 'visited' : 6, 'path' : 7}
INIT_SNAKE_PARTS_NUM = 3
INIT_SNAKE1_ID : tuple[int, int] = (5, 5)
INIT_SNAKE2_ID : tuple[int, int] = (5, 8)
INIT_FOOD_ID = (10, 5)
INIT_NOISES: list[tuple[int, int]] = []
DIRECTION_DICT: dict[str, tuple[int, int]] = {'right' : (1, 0), 'down' : (0, 1), 'left' : (-1, 0), 'up' : (0, -1)}