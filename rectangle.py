import pygame
from constants import *

class Rectangle:
    def __init__(self, surface, position, width, height, border_color = BORDER_COLOR, bg_color = BACKGROUND_COLOR):
        self.surface = surface
        self.position = position
        self.width = width
        self.height = height
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.border_color = border_color
        self.bg_color = bg_color
        
    def draw_border(self):
        pygame.draw.line(self.surface, self.border_color, (self.position[0], self.position[1]), (self.position[0] + self.width, self.position[1]))
        pygame.draw.line(self.surface, self.border_color, (self.position[0], self.position[1]), (self.position[0], self.position[1] + self.height))
        pygame.draw.line(self.surface, self.border_color, (self.position[0] + self.width, self.position[1]), (self.position[0] + self.width, self.position[1] + self.height))
        pygame.draw.line(self.surface, self.border_color, (self.position[0], self.position[1] + self.height), (self.position[0] + self.width, self.position[1] + self.height))

    def fill_color(self):
        pygame.draw.rect(self.surface, self.bg_color, self.rect)