import pygame
from constant import *

class Rectangle:
    def __init__(self, surface: pygame.Surface, position: tuple[int, int], width: int, height: int, border_color = BORDER_COLOR, fill_color = BACKGROUND_COLOR, image_path = '') -> None:
        self.surface = surface
        self.position = position
        self.width = width
        self.height = height
        self.border_color = border_color
        self.fill_color = fill_color
        self.rect = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        self.has_image = True
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except FileNotFoundError:
            self.has_image = False
        
    def draw_border(self) -> None:
        pygame.draw.line(self.surface, self.border_color, (self.position[0], self.position[1]), (self.position[0] + self.width, self.position[1]))
        pygame.draw.line(self.surface, self.border_color, (self.position[0], self.position[1]), (self.position[0], self.position[1] + self.height))
        pygame.draw.line(self.surface, self.border_color, (self.position[0] + self.width, self.position[1]), (self.position[0] + self.width, self.position[1] + self.height))
        pygame.draw.line(self.surface, self.border_color, (self.position[0], self.position[1] + self.height), (self.position[0] + self.width, self.position[1] + self.height))

    def fill(self) -> None:
        if self.has_image:
            self.surface.blit(self.image, self.position)
        else:
            pygame.draw.rect(self.surface, self.fill_color, self.rect)

    def is_clicked(self, event: pygame.event.Event, mouse: tuple[int, int]) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mouse[0], mouse[1]):
            return True
        return False