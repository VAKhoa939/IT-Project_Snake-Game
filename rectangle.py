import pygame
from constant import *

class Rectangle:
    def __init__(self, surface : pygame.Surface, position : tuple[int, int], width : int, height : int, border_color = BORDER_COLOR, fill_color = BACKGROUND_COLOR):
        self.surface = surface
        self.position = position
        self.width = width
        self.height = height
        self.border_color = border_color
        self.fill_color = fill_color
        
    def draw_border(self):
        pygame.draw.line(self.surface, self.border_color, (self.position[0], self.position[1]), (self.position[0] + self.width, self.position[1]))
        pygame.draw.line(self.surface, self.border_color, (self.position[0], self.position[1]), (self.position[0], self.position[1] + self.height))
        pygame.draw.line(self.surface, self.border_color, (self.position[0] + self.width, self.position[1]), (self.position[0] + self.width, self.position[1] + self.height))
        pygame.draw.line(self.surface, self.border_color, (self.position[0], self.position[1] + self.height), (self.position[0] + self.width, self.position[1] + self.height))

    def fill(self):
        pygame.draw.rect(self.surface, self.fill_color, pygame.Rect(self.position[0], self.position[1], self.width, self.height))

    def is_clicked(self, event : pygame.event.Event, mouse : tuple[int, int]):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse[0] > self.position[0] and mouse[0] < self.position[0] + self.width:
                if mouse[1] > self.position[1] and mouse[1] < self.position[1] + self.height:
                    return True
        return False