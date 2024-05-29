import pygame
import math
from pygame.locals import *
from board import *
from constant import *
from control import *

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Snake Game')
        self.fps_controller = pygame.time.Clock()
        self.fps_value = FPS
        self.window = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        self.window_width, self.window_height = self.window.get_size()
        try:
            self.background = pygame.transform.scale(pygame.image.load('images/background.png'), self.window.get_size())
        except FileNotFoundError:
            print("Error: File 'background.png' not found.")
            self.background = None
        self.board = Board(self.window)
        self.page = 1
        self.is_two_player = True

        # Page 1: The Settings Page
        self.lbl_player = Textbox(self.window, (1420, 100), 300, 50, 'Number of players:')
        self.btn_player1 = Button(self.window, (1370, 200), '1 Player')
        self.btn_player2 = Button(self.window, (1620, 200), '2 Players')
        self.lbl_mode_title_player1 = Textbox(self.window, (1270, 300), 300, 50, 'Mode for Player 1:')
        self.cbb_mode_player1 = ComboBox(self.window, (1270, 400), 300, 50, 'Manual', MODE_NAMES)
        self.lbl_mode_title_player2 = Textbox(self.window, (1600, 300), 300, 50, 'Mode for Player 2:')
        self.cbb_mode_player2 = ComboBox(self.window, (1600, 400), 300, 50, 'Manual', MODE_NAMES)
        self.btn_continue = Button(self.window, (1500, 800), 'Continue')
        self.btn_quit = Button(self.window, (1500, 900), 'Quit')

        # Page 2: The Main Page
        self.lbl_status = Textbox(self.window, (1420, 50), 300, 50, 'Waiting', prefix = 'Status: ')
        self.lbl_dead = Textbox(self.window, (1420, 100), 300, 50, ' died')
        self.timer = Timer(self.window, (1420, 150), 300, 50)
        self.lbl_speed = Textbox(self.window, (1420, 200), 300, 50, 'x1.0', prefix = 'Speed: ')
        self.btn_slow = Button(self.window, (1420, 300), 'x0.5')
        self.btn_normal = Button(self.window, (1580, 300), 'x1.0')
        self.btn_fast = Button(self.window, (1420, 400), 'x2.0')
        self.btn_very_fast = Button(self.window, (1580, 400), 'x4.0')
        self.btn_play = Button(self.window, (1500, 500), 'Play')
        self.btn_pause = Button(self.window, (1500, 600), 'Pause')
        self.btn_reset = Button(self.window, (1500, 700), 'Reset')
        self.btn_edit = Button(self.window, (1500, 800), 'Edit')
        self.btn_back = Button(self.window, (1500, 900), 'Back')
        self.lbl_statistic_player1 = Textbox(self.window, (100, 700), 300, 50, 'Player 1 (Green):')
        self.lbl_length_player1 = Textbox(self.window, (100, 750), 300, 50, '0', prefix = 'Length: ')
        self.lbl_mode_player1 = Textbox(self.window, (100, 800), 300, 50, '', prefix = 'Mode: ')
        self.lbl_manual_player1 = Textbox(self.window, (100, 850), 300, 50, 'Use Arrow Keys')
        self.lbl_statistic_player2 = Textbox(self.window, (700, 700), 300, 50, 'Player 2 (Orange):')
        self.lbl_length_player2 = Textbox(self.window, (700, 750), 300, 50, '0', prefix = 'Length: ')
        self.lbl_mode_player2 = Textbox(self.window, (700, 800), 300, 50, '', prefix = 'Mode: ')
        self.lbl_manual_player2 = Textbox(self.window, (700, 850), 300, 50, 'Use WASD Keys')
        self.btn_show_path = Button(self.window, (700, 700), 'Show Path')
        self.btn_hide_path = Button(self.window, (870, 700), 'Hide Path')
        self.lbl_node = Textbox(self.window, (700, 750), 300, 50, '0', prefix = 'Node: ')
        self.lbl_depth = Textbox(self.window, (700, 800), 300, 50, '0', prefix = 'Depth: ')

        # Page 3: The Edit Page
        self.lbl_note = Textbox(self.window, (1320, 100), 500, 50, 'Remember to save before go back')
        self.btn_reset_edit = Button(self.window, (1500, 200), 'Reset')
        self.btn_save_edit = Button(self.window, (1500, 300), 'Save')
        self.cbb_object = ComboBox(self.window, (1420, 400), 300, 50, 'Choose object', OBJECT_NAMES)
        self.btn_back_edit = Button(self.window, (1500, 800), 'Back')

    def draw(self) -> None:
        if self.background:
            self.window.blit(self.background, (0, 0))
        self.board.draw()
        if self.page == 1:
            self.draw_ui_1st_page()
        elif self.page == 2:
            self.draw_ui_2nd_page()
        elif self.page == 3:
            self.draw_ui_3rd_page()

    def draw_ui_1st_page(self) -> None:
        self.lbl_player.draw()
        self.btn_player1.draw()
        self.btn_player2.draw()
        self.btn_continue.draw()
        self.btn_quit.draw()
        self.lbl_mode_title_player1.draw()
        self.cbb_mode_player1.draw()
        if self.is_two_player:
            self.lbl_mode_title_player2.draw()
            self.cbb_mode_player2.draw()

    def draw_ui_2nd_page(self) -> None:
        self.lbl_status.draw()
        if self.lbl_status.text == 'GAME OVER!':
            self.lbl_dead.draw()
        if self.lbl_status.text == 'Playing':
            self.timer.time_to_text()
        self.timer.draw()
        self.lbl_speed.draw()
        self.btn_slow.draw()
        self.btn_normal.draw()
        self.btn_fast.draw()
        self.btn_very_fast.draw()
        self.btn_play.draw()
        self.btn_pause.draw()
        self.btn_reset.draw()
        self.btn_edit.draw()
        self.btn_back.draw()

        self.lbl_statistic_player1.draw()
        self.lbl_length_player1.text = str(self.board.snake1.length)
        self.lbl_length_player1.draw()
        self.lbl_mode_player1.text = self.cbb_mode_player1.text
        self.lbl_mode_player1.draw()
        if not self.is_two_player:
            if self.cbb_mode_player1.text != 'Manual':
                self.btn_show_path.draw()
                self.btn_hide_path.draw()
                self.lbl_node.draw()
                self.lbl_depth.draw()
            else:
                self.lbl_manual_player1.draw()
        else:
            self.lbl_statistic_player2.draw()
            self.lbl_length_player2.text = str(self.board.snake2.length)
            self.lbl_length_player2.draw()
            self.lbl_mode_player2.text = self.cbb_mode_player2.text
            self.lbl_mode_player2.draw()
            if self.cbb_mode_player1.text == 'Manual':
                self.lbl_manual_player1.draw()
            if self.cbb_mode_player2.text == 'Manual':
                self.lbl_manual_player2.draw()

    def draw_ui_3rd_page(self) -> None:
        self.lbl_note.draw()
        self.btn_reset_edit.draw()
        self.btn_save_edit.draw()
        self.cbb_object.draw()
        self.btn_back_edit.draw()

    def handle_events(self, event: pygame.event.Event, mouse: tuple[int, int]) -> None:
        if self.page == 1:
            self.handle_1st_page(event, mouse)
        elif self.page == 2:
            self.handle_2nd_page(event, mouse)
        elif self.page == 3:
            self.handle_3rd_page(event, mouse)

    def handle_1st_page(self, event: pygame.event.Event, mouse: tuple[int, int]):
        if self.btn_player1.is_clicked(event, mouse):
            self.is_two_player = self.board.is_two_player = False
        
        if self.btn_player2.is_clicked(event, mouse):
            self.is_two_player = self.board.is_two_player = True
        
        self.cbb_mode_player1.is_clicked(event, mouse)
        self.cbb_mode_player2.is_clicked(event, mouse)
        
        if self.btn_continue.is_clicked(event, mouse):
            self.page = 2
        
        if self.btn_quit.is_clicked(event, mouse):
            pygame.quit()
            exit()

    def handle_2nd_page(self, event: pygame.event.Event, mouse: tuple[int, int]):
        if self.btn_slow.is_clicked(event, mouse):
            self.lbl_speed.text = self.btn_slow.text
            self.fps_value = FPS // 2

        if self.btn_normal.is_clicked(event, mouse):
            self.lbl_speed.text = self.btn_normal.text
            self.fps_value = FPS

        if self.btn_fast.is_clicked(event, mouse):
            self.lbl_speed.text = self.btn_fast.text
            self.fps_value = FPS * 2

        if self.btn_very_fast.is_clicked(event, mouse):
            self.lbl_speed.text = self.btn_very_fast.text
            self.fps_value = FPS * 4

        if self.lbl_status.text == 'Playing':
            if self.cbb_mode_player1.text == 'Manual':
                self.board.snake1.handle_keys()

            if self.is_two_player and self.cbb_mode_player2.text == 'Manual':
                self.board.snake2.handle_keys()

        if self.lbl_status.text != 'GAME OVER!':
            if self.btn_play.is_clicked(event, mouse):
                self.timer.start()
                self.lbl_status.text = 'Playing'

            if self.btn_pause.is_clicked(event, mouse):
                self.timer.pause()
                self.lbl_status.text = 'Paused'

        if self.lbl_status.text != 'Playing':
            if self.btn_reset.is_clicked(event, mouse):
                self.timer.reset()
                self.board.reset()
                self.lbl_status.text = 'Waiting'

            if self.btn_edit.is_clicked(event, mouse):
                self.board.reset()
                self.lbl_status.text = 'Waiting'
                self.page = 3
                self.board.is_two_player = True

            if self.btn_back.is_clicked(event, mouse):
                self.board.reset()
                self.lbl_status.text = 'Waiting'
                self.page = 1
        
        if self.btn_show_path.is_clicked(event, mouse):
            self.board.allow_show_path = True

        if self.btn_hide_path.is_clicked(event, mouse):
            self.board.allow_show_path = False

    def handle_3rd_page(self, event: pygame.event.Event, mouse: tuple[int, int]) -> None:
        if self.cbb_object.text != self.cbb_object.defaut_option:
            if self.board.is_editing(event, mouse, self.cbb_object.text):
                self.lbl_note.text = 'The board state is unsaved'
        
        if self.btn_reset_edit.is_clicked(event, mouse):
            self.lbl_note.text = 'The board state has been reset'
            self.board.reset()
        
        if self.btn_save_edit.is_clicked(event, mouse):
            self.lbl_note.text = 'The board state has been saved'
            self.board.save()
        self.cbb_object.is_clicked(event, mouse)
        
        if self.btn_back_edit.is_clicked(event, mouse):
            self.lbl_note.text = 'Remember to save before go back'
            self.board.reset()
            self.page = 2
            self.board.is_two_player = True if self.is_two_player else False

    def play(self) -> None:
        if not self.is_two_player:
            self.play_single_player()
        else:
            self.play_two_players()

    def play_single_player(self) -> None:
        if self.board.snake1.is_food_found(self.board.food_id):
            self.board.respawn_food()

        if self.board.snake1.is_dead():
            self.lbl_status.text = 'GAME OVER!'
            self.lbl_dead.prefix = 'Player 1'
            return

        if self.cbb_mode_player1.text != 'Manual':
            self.board.snake1.find_path(self.cbb_mode_player1.text, self.board.food_id)
            self.lbl_node.text = str(self.board.snake1.algorithm.node_num)
            self.lbl_depth.text = str(self.board.snake1.algorithm.max_depth)
        
        self.board.snake1.set_direction()
        self.board.snake1.move()

    def play_two_players(self) -> None:
        if self.board.snake1.is_food_found(self.board.food_id) or self.board.snake2.is_food_found(self.board.food_id):
            self.board.respawn_food()

        if self.board.snake1.is_dead(self.board.snake2.parts):
            self.lbl_status.text = 'GAME OVER!'
            self.lbl_dead.prefix = 'Player 1'
            return
        
        if self.board.snake2.is_dead(self.board.snake1.parts):
            self.lbl_status.text = 'GAME OVER!'
            self.lbl_dead.prefix = 'Player 2'
            return

        if self.cbb_mode_player1.text != 'Manual':
            self.board.snake1.find_path(self.cbb_mode_player1.text, self.board.food_id, self.board.snake2.parts)

        if self.cbb_mode_player2.text != 'Manual':
            self.board.snake2.find_path(self.cbb_mode_player2.text, self.board.food_id, self.board.snake1.parts)
        
        self.board.snake1.set_direction()
        self.board.snake1.move()
        self.board.snake2.set_direction()
        self.board.snake2.move()

def main() -> None:
    game = Game()
    game.draw()
    while True:
        events = pygame.event.get()
        mouse = pygame.mouse.get_pos()
        for event in events:
            if event.type == QUIT: # Default exit
                pygame.quit()
                exit()
            game.handle_events(event, mouse)
        if game.lbl_status.text == 'Playing':
            game.play()
        game.draw()
        game.timer.count()
        pygame.display.update()
        game.fps_controller.tick(game.fps_value)

if __name__ == "__main__":
    main()