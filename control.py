import pygame
from pygame.event import Event
from constant import *
from shape import *

class Textbox(Rectangle):
    def __init__(self, surface: pygame.Surface, position: tuple[int, int], width: int, height: int, text = '', prefix = '', border_color = BACKGROUND_COLOR, fill_color = BACKGROUND_COLOR, text_color = TEXT_COLOR, text_font = TEXT_FONT, text_size = TEXT_SIZE, image_path = '') -> None:
        super().__init__(surface, position, width, height, border_color = border_color, fill_color = fill_color, image_path = image_path)
        self.prefix = prefix
        self.text = text 
        self.text_color = text_color
        self.text_size = text_size
        self.text_font = pygame.font.SysFont(text_font, self.text_size, bold=True)
    
    def draw(self) -> None:
        if not self.has_image:
            self.draw_border()
        self.fill()
        label = self.text_font.render(self.prefix + self.text, True, self.text_color)
        self.surface.blit(label, (self.position[0] + (self.width // 2 - label.get_width() // 2), self.position[1] + (self.height // 2 - label.get_height() // 2)))

class Button(Textbox):
    def __init__(self, surface: pygame.Surface, position: tuple[int, int], width: int, height: int, text = '', border_color = BORDER_COLOR, fill_color = BUTTON_COLOR, image_path = '') -> None:
        super().__init__(surface, position, width, height, text, border_color = border_color, fill_color = fill_color, image_path = image_path)

class ComboBox(Button):
    def __init__(self, surface: pygame.Surface, position: tuple[int, int], width: int, height: int, defaut_option: str, options: list[str], image_path = '') -> None:
        super().__init__(surface, position, width, height, defaut_option, BORDER_COLOR, image_path = image_path)
        self.defaut_option = defaut_option
        self.btn_options: list[Button] = []
        for i, option in enumerate(options):
            self.btn_options.append(Button(self.surface, (self.position[0], self.position[1] + (i + 1) * height), self.width, self.height, option, self.border_color, OPTION_COLOR))
        self.is_open = False

    def draw(self) -> None:
        super().draw()
        if self.is_open:
            for btn_option in self.btn_options:
                btn_option.draw()

    def is_clicked(self, event: Event, mouse: tuple[int, int]) -> None:
        if super().is_clicked(event, mouse):
            self.is_open = False if self.is_open else True
        if self.is_open:
            for btn_option in self.btn_options:
                if not btn_option.is_clicked(event, mouse):
                    continue
                self.text = self.defaut_option if btn_option.text == '(None)' else btn_option.text
                self.is_open = False
                return
            
class Timer(Textbox):
    def __init__(self, surface: pygame.Surface, position: tuple[int, int], width: int, height: int) -> None:
        super().__init__(surface, position, width, height, text = '0:00', prefix = 'Time: ')
        self.start_time = 0
        self.end_time = 0
        self.milisecond = 0

    def time_to_text(self) -> None:
        second = (self.milisecond + self.end_time - self.start_time) // 1000
        minute = second // 60
        second = second % 60
        self.text = '0' if minute == 0 else str(minute)
        self.text += ':' 
        self.text += ('0' + str(second)) if second < 10 else str(second)

    def start(self) -> None:
        self.start_time = self.end_time = pygame.time.get_ticks()

    def count(self) -> None:
        self.end_time = pygame.time.get_ticks()

    def pause(self) -> None:
        self.milisecond += (self.end_time - self.start_time)

    def reset(self) -> None:
        self.start_time = self.end_time = self.milisecond = 0
        self.text = '0:00'
        
