import pygame
import math
from pygame.locals import *
from board import *
from constants import *
from button import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Pygame practice')
        self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.window.fill(BACKGROUND_COLOR)
        self.board = Board(self.window)
        self.btn_exit = ExitButton(self.window, [1350, 50], 150, 50, RED)

    def draw(self):
        self.board.draw()
        self.btn_exit.draw()
        

game = Game()
game.draw()
active_events = 0
while True:
    active_events = 0
    events = pygame.event.get()
    mouse = pygame.mouse.get_pos()
    for event in events:
        if event.type == QUIT: # Default exit
            pygame.quit()
            exit()
        game.btn_exit.is_clicked(event, mouse)
        active_events += game.board.is_clicked(event, mouse)
    if active_events > 0:
        game.draw()
    pygame.display.update()