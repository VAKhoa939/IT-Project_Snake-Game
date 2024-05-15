import pygame
import math
from pygame.locals import *
from board import *
from constant import *
from button import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snake Game')
        self.fps_controller = pygame.time.Clock()
        self.window = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        self.board = Board(self.window)
        self.page = 1
        self.is_two_player = True
        self.lbl_status = Textbox(self.window, (1350, 100), 150, 50, 'Waiting', prefix = 'Status: ')

        # Page 1
        self.lbl_player = Textbox(self.window, (1300, 100), 250, 50, 'Number of players:')
        self.btn_player1 = Button(self.window, (1300, 150), 140, 50, '1 Player')
        self.btn_player2 = Button(self.window, (1450, 150), 140, 50, '2 Players')
        self.lbl_mode_player1 = Textbox(self.window, (1300, 250), 250, 50, 'Mode for Player 1:')
        self.cbb_mode_player1 = ComboBox(self.window, (1300, 300), 250, 50, 'Manual', MODE_NAMES)
        self.lbl_mode_player2 = Textbox(self.window, (1300, 400), 250, 50, 'Mode for Player 2:')
        self.cbb_mode_player2 = ComboBox(self.window, (1300, 450), 250, 50, 'Manual', MODE_NAMES)
        self.btn_next = Button(self.window, (1350, 700), 150, 50, 'Continue')
        self.btn_quit = Button(self.window, (1350, 800), 150, 50, 'Quit')

        # Page 2
        self.lbl_score_player1 = Textbox(self.window, (1350, 200), 150, 50, '0', prefix = 'Player 1 Score: ')
        self.lbl_score_player2 = Textbox(self.window, (1350, 300), 150, 50, '0', prefix = 'Player 2 Score: ')
        self.btn_play = Button(self.window, (1350, 400), 150, 50, 'Play')
        self.btn_pause = Button(self.window, (1350, 500), 150, 50, 'Pause')
        self.btn_reset = Button(self.window, (1350, 600), 150, 50, 'Reset')
        self.btn_edit = Button(self.window, (1350, 700), 150, 50, 'Edit Mode')
        self.btn_back1 = Button(self.window, (1350, 800), 150, 50, 'Go Back')

        # Page 3
        self.btn_reset_edit = Button(self.window, (1350, 200), 150, 50, 'Reset')
        self.btn_save_edit = Button(self.window, (1350, 300), 150, 50, 'Save')
        self.cbb_object = ComboBox(self.window, (1300, 400), 250, 50, 'Choose object', OBJECT_NAMES)
        self.btn_back2 = Button(self.window, (1350, 800), 150, 50, 'Go Back')

    def draw(self):
        self.window.fill(BACKGROUND_COLOR)
        self.board.draw()
        if self.page == 1:
            self.draw_ui_1st_page()
        elif self.page == 2:
            self.draw_ui_2nd_page()
        elif self.page == 3:
            self.draw_ui_3rd_page()

    def draw_ui_1st_page(self):        
        self.lbl_player.draw()
        self.btn_player1.draw()
        self.btn_player2.draw()
        self.lbl_mode_player1.draw()
        self.cbb_mode_player1.draw()
        if self.is_two_player and not self.cbb_mode_player1.is_open:
            self.lbl_mode_player2.draw()
            self.cbb_mode_player2.draw()
        if not self.cbb_mode_player2.is_open:
            self.btn_next.draw()
            self.btn_quit.draw()

    def draw_ui_2nd_page(self):
        self.lbl_status.draw()
        self.lbl_score_player1.text = str(self.board.snake1.score)
        self.lbl_score_player1.draw()
        if self.is_two_player:
            self.lbl_score_player2.text = str(self.board.snake2.score)
            self.lbl_score_player2.draw()
        self.btn_play.draw()
        self.btn_pause.draw()
        self.btn_reset.draw()
        self.btn_edit.draw()
        self.btn_back1.draw()

    def draw_ui_3rd_page(self):
        self.lbl_status.draw()
        self.btn_reset_edit.draw()
        self.btn_save_edit.draw()
        self.cbb_object.draw()
        self.btn_back2.draw()

    def handle_events(self, event : pygame.event.Event, mouse : tuple[int, int]):
        if self.page == 1:
            self.handle_1st_page(event, mouse)
        elif self.page == 2:
            self.handle_2nd_page(event, mouse)
        elif self.page == 3:
            self.handle_3rd_page(event, mouse)

    def handle_1st_page(self, event : pygame.event.Event, mouse : tuple[int, int]):
        if self.btn_player1.is_clicked(event, mouse):
            self.is_two_player = self.board.is_two_player = False
        if self.btn_player2.is_clicked(event, mouse):
            self.is_two_player = self.board.is_two_player = True
        if not self.cbb_mode_player1.is_open and not self.cbb_mode_player2.is_open:
            if self.btn_next.is_clicked(event, mouse):
                self.page = 2
            if self.btn_quit.is_clicked(event, mouse):
                pygame.quit()
                exit()
        if self.is_two_player and not self.cbb_mode_player1.is_open:
            self.cbb_mode_player2.is_clicked(event, mouse)
        self.cbb_mode_player1.is_clicked(event, mouse)

    def handle_2nd_page(self, event : pygame.event.Event, mouse : tuple[int, int]):
        if self.lbl_status.text == 'Playing':
            if self.cbb_mode_player1.text == 'Manual':
                self.board.snake1.handle_keys()
            if self.is_two_player and self.cbb_mode_player2.text == 'Manual':
                self.board.snake2.handle_keys()
        if self.btn_reset.is_clicked(event, mouse):
            self.board.reset()
            self.lbl_status.text = 'Waiting'
        if self.lbl_status.text != 'GAME OVER!':
            if self.btn_play.is_clicked(event, mouse):
                self.lbl_status.text = 'Playing'
            if self.btn_pause.is_clicked(event, mouse):
                self.lbl_status.text = 'Paused'
        if self.lbl_status.text != 'Playing':
            if self.btn_reset.is_clicked(event, mouse):
                self.board.reset()
                self.lbl_status.text = 'Waiting'
            if self.btn_edit.is_clicked(event, mouse):
                self.board.reset()
                self.lbl_status.text = 'Waiting'
                self.page = 3
            if self.btn_back1.is_clicked(event, mouse):
                self.board.reset()
                self.lbl_status.text = 'Waiting'
                self.page = 1

    def handle_3rd_page(self, event : pygame.event.Event, mouse : tuple[int, int]):
        if self.cbb_object.text != self.cbb_object.defaut_option:
            self.lbl_status.text = self.board.is_clicked(event, mouse, self.cbb_object.text)
        if self.btn_reset_edit.is_clicked(event, mouse):
            self.board.reset()
            self.lbl_status.text = 'Reset'
        if self.btn_save_edit.is_clicked(event, mouse):
            self.board.save()
            self.lbl_status.text = 'Saved'
        self.cbb_object.is_clicked(event, mouse)
        if self.btn_back2.is_clicked(event, mouse):
            self.board.reset()
            self.lbl_status.text = 'Waiting'
            self.page = 2

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
        if not game.is_two_player:
            if game.cbb_mode_player1.text != 'Manual':
                game.lbl_status.text = game.board.snake1.find_path(game.cbb_mode_player1.text, game.board.food_id)
            game.board.snake1.move()
            if game.board.snake1.is_food_found(game.board.food_id):
                game.board.respawn_food()
            if game.board.snake1.is_dead():
                game.lbl_status.text = 'GAME OVER!'
        else:
            if game.cbb_mode_player1.text != 'Manual':
                game.lbl_status.text = game.board.snake1.find_path(game.cbb_mode_player1.text, game.board.food_id, game.board.snake2.get_parts_id())
            if game.cbb_mode_player2.text != 'Manual':
                game.lbl_status.text = game.board.snake2.find_path(game.cbb_mode_player2.text, game.board.food_id, game.board.snake1.get_parts_id())
            game.board.snake1.move()
            game.board.snake2.move()
            if game.board.snake1.is_food_found(game.board.food_id) or game.board.snake2.is_food_found(game.board.food_id):
                game.board.respawn_food()
            if game.board.snake1.is_dead(game.board.snake2.parts) or game.board.snake2.is_dead(game.board.snake1.parts):
                game.lbl_status.text = 'GAME OVER!'
    game.draw()
    pygame.display.update()
    game.fps_controller.tick(20)