import pygame
from pygame.event import Event
from constant import *
from rectangle import *

class Textbox(Rectangle):
    def __init__(self, surface : pygame.Surface, position : tuple[int, int], width : int, height : int, text : str, prefix = '', border_color = BACKGROUND_COLOR, fill_color = BACKGROUND_COLOR, text_color = TEXT_COLOR, text_font = TEXT_FONT, text_size = TEXT_SIZE):
        super().__init__(surface, position, width, height, border_color = border_color, fill_color = fill_color)
        self.prefix = prefix
        self.text = text 
        self.text_color = text_color
        self.text_size = text_size
        self.text_font = pygame.font.SysFont(text_font, self.text_size, bold=True)
    
    def draw(self):
        self.draw_border()
        self.fill()
        label = self.text_font.render(self.prefix + self.text, True, self.text_color)
        self.surface.blit(label, (self.position[0] + (self.width // 2 - label.get_width() // 2), self.position[1] + (self.height // 2 - label.get_height() // 2)))

class Button(Textbox):
    def __init__(self, surface : pygame.Surface, position : tuple[int, int], width : int, height : int, text : str, border_color = BORDER_COLOR, fill_color = BUTTON_COLOR):
        super().__init__(surface, position, width, height, text, border_color = border_color, fill_color = fill_color)

class ComboBox(Button):
    def __init__(self, surface : pygame.Surface, position : tuple[int, int], width : int, height : int, defaut_option : str, options : list[str]):
        super().__init__(surface, position, width, height, defaut_option, BORDER_COLOR, COMBOBOX_COLOR)
        self.defaut_option = defaut_option
        self.btn_options : list[Button] = []
        for i, option in enumerate(options):
            self.btn_options.append(Button(self.surface, (self.position[0], self.position[1] + (i + 1) * height), self.width, self.height, option, self.border_color, OPTION_COLOR))
        self.is_open = False

    def draw(self):
        super().draw()
        if self.is_open:
            for btn_option in self.btn_options:
                btn_option.draw()

    def is_clicked(self, event : Event, mouse : tuple[int, int]):
        if super().is_clicked(event, mouse):
            self.is_open = False if self.is_open else True
        if self.is_open:
            for btn_option in self.btn_options:
                if not btn_option.is_clicked(event, mouse):
                    continue
                self.text = self.defaut_option if btn_option.text == '(None)' else btn_option.text
                self.is_open = False
                return