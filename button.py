import pygame, events
from constants import *
from rectangle import *

class Textbox(Rectangle):
    def __init__(self, surface, position, width, height, bg_color, text=' '):
        super().__init__(surface, position, width, height, BORDER_COLOR, bg_color)
        self.text = text 
        self.font = pygame.font.SysFont('Consolas', 25)
        self.text = self.font.render(self.text, True, WHITE)
    
    def draw(self):
        self.draw_border()
        self.fill_color()
        self.surface.blit(self.text, (self.position[0] + (self.width/2 - self.text.get_width()/2), self.position[1] + (self.height/2 - self.text.get_height()/2)))

class ExitButton(Textbox):
    def __init__(self, surface, position, width, height, bg_color):
        super().__init__(surface, position, width, height, bg_color, 'Quit')

    def is_clicked(self, event, mouse):
        if events.is_clicked(self, event, mouse):
            pygame.quit()
            exit()