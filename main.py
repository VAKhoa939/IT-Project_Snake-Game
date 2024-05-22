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
        self.window = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
        self.board = Board(self.window)
        self.page = 1
        self.is_two_player = True
        self.lbl_status = Textbox(self.window, (1350, 50), 150, 50, 'Waiting', prefix = 'Status: ')

        # Page 1
        self.lbl_player = Textbox(self.window, (1300, 100), 250, 50, 'Number of players:')
        self.btn_player1 = Button(self.window, (1300, 150), 140, 50, '1 Player')
        self.btn_player2 = Button(self.window, (1450, 150), 140, 50, '2 Players')
        self.lbl_mode_title_player1 = Textbox(self.window, (1300, 250), 250, 50, 'Mode for Player 1:')
        self.cbb_mode_player1 = ComboBox(self.window, (1300, 300), 250, 50, 'Manual', MODE_NAMES)
        self.lbl_mode_title_player2 = Textbox(self.window, (1300, 400), 250, 50, 'Mode for Player 2:')
        self.cbb_mode_player2 = ComboBox(self.window, (1300, 450), 250, 50, 'Manual', MODE_NAMES)
        self.btn_next = Button(self.window, (1350, 700), 150, 50, 'Continue')
        self.btn_quit = Button(self.window, (1350, 800), 150, 50, 'Quit')

        # Page 2
        self.timer = Timer(self.window, (1350, 150), 150, 50)
        self.lbl_dead = Textbox(self.window, (1350, 250), 150, 50, ' died')
        self.btn_play = Button(self.window, (1350, 400), 150, 50, 'Play')
        self.btn_pause = Button(self.window, (1350, 500), 150, 50, 'Pause')
        self.btn_reset = Button(self.window, (1350, 600), 150, 50, 'Reset')
        self.btn_edit = Button(self.window, (1350, 700), 150, 50, 'Edit Mode')
        self.btn_back1 = Button(self.window, (1350, 800), 150, 50, 'Go Back')
        self.lbl_statistic_player1 = Textbox(self.window, (100, 700), 150, 50, 'Player 1: ')
        self.lbl_score_player1 = Textbox(self.window, (100, 750), 150, 50, '0', prefix = '- Score: ')
        self.lbl_mode_player1 = Textbox(self.window, (100, 800), 200, 50, '', prefix = '- Mode: ')
        self.lbl_statistic_player2 = Textbox(self.window, (700, 700), 150, 50, 'Player 2: ')
        self.lbl_score_player2 = Textbox(self.window, (700, 750), 150, 50, '0', prefix = '- Score: ')
        self.lbl_mode_player2 = Textbox(self.window, (700, 800), 200, 50, '', prefix = '- Mode: ')
        self.lbl_node = Textbox(self.window, (700, 750), 150, 50, '0', prefix = '- Node: ')
        self.lbl_depth = Textbox(self.window, (700, 800), 150, 50, '0', prefix = '- Depth: ')

        # Page 3
        self.btn_reset_edit = Button(self.window, (1350, 200), 150, 50, 'Reset')
        self.btn_save_edit = Button(self.window, (1350, 300), 150, 50, 'Save')
        self.cbb_object = ComboBox(self.window, (1300, 400), 250, 50, 'Choose object', OBJECT_NAMES)
        self.btn_back2 = Button(self.window, (1350, 800), 150, 50, 'Go Back')

    def draw(self) -> None:
        self.window.fill(BACKGROUND_COLOR)
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
        self.lbl_mode_title_player1.draw()
        self.cbb_mode_player1.draw()
        if self.is_two_player and not self.cbb_mode_player1.is_open:
            self.lbl_mode_title_player2.draw()
            self.cbb_mode_player2.draw()
        if not self.cbb_mode_player2.is_open:
            self.btn_next.draw()
            self.btn_quit.draw()

    def draw_ui_2nd_page(self) -> None:
        self.lbl_status.draw()
        if self.lbl_status.text == 'Playing':
            self.timer.time_to_text()
        self.timer.draw()
        if self.lbl_status.text == 'GAME OVER!':
            self.lbl_dead.draw()
        self.btn_play.draw()
        self.btn_pause.draw()
        self.btn_reset.draw()
        self.btn_edit.draw()
        self.btn_back1.draw()

        self.lbl_statistic_player1.draw()
        self.lbl_score_player1.text = str(self.board.snake1.score)
        self.lbl_score_player1.draw()
        self.lbl_mode_player1.text = self.cbb_mode_player1.text
        self.lbl_mode_player1.draw()
        if not self.is_two_player:
            if self.cbb_mode_player1.text != 'Manual':
                self.lbl_node.draw()
                self.lbl_depth.draw()
        else:
            self.lbl_statistic_player2.draw()
            self.lbl_score_player2.text = str(self.board.snake2.score)
            self.lbl_score_player2.draw()
            self.lbl_mode_player2.text = self.cbb_mode_player2.text
            self.lbl_mode_player2.draw()

    def draw_ui_3rd_page(self) -> None:
        self.lbl_status.draw()
        self.btn_reset_edit.draw()
        self.btn_save_edit.draw()
        self.cbb_object.draw()
        self.btn_back2.draw()

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
        
        if not self.cbb_mode_player1.is_open and not self.cbb_mode_player2.is_open:
            if self.btn_next.is_clicked(event, mouse):
                self.page = 2
            
            if self.btn_quit.is_clicked(event, mouse):
                pygame.quit()
                exit()
        
        if self.is_two_player and not self.cbb_mode_player1.is_open:
            self.cbb_mode_player2.is_clicked(event, mouse)
        self.cbb_mode_player1.is_clicked(event, mouse)

    def handle_2nd_page(self, event: pygame.event.Event, mouse: tuple[int, int]):
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

            if self.btn_back1.is_clicked(event, mouse):
                self.board.reset()
                self.lbl_status.text = 'Waiting'
                self.page = 1

    def handle_3rd_page(self, event: pygame.event.Event, mouse: tuple[int, int]) -> None:
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

        if self.cbb_mode_player1.text != 'Manual' and self.board.snake1.algorithm.food_id != self.board.food_id:
            self.board.snake1.find_path(self.cbb_mode_player1.text, self.board.food_id)
            self.lbl_node.text = str(self.board.snake1.algorithm.node_num)
            self.lbl_depth.text = str(self.board.snake1.algorithm.max_depth)
        
        self.board.snake1.set_direction()
        self.board.snake1.move()

    def play_two_players(self) -> None:
        if self.board.snake1.is_food_found(self.board.food_id) or self.board.snake2.is_food_found(self.board.food_id):
            self.board.respawn_food()

        # First snake's move
        if self.board.snake1.is_dead(self.board.snake2.parts):
            self.lbl_status.text = 'GAME OVER!'
            self.lbl_dead.prefix = 'Player 1'
            return

        if self.cbb_mode_player1.text != 'Manual' and self.board.snake1.algorithm.food_id != self.board.food_id:
            self.board.snake1.find_path(self.cbb_mode_player1.text, self.board.food_id, self.board.snake2.parts)
        
        self.board.snake1.set_direction()
        if self.cbb_mode_player1.text != 'Manual' and self.board.snake1.is_near_dead(self.board.snake2.parts):
            self.board.snake1.find_path(self.cbb_mode_player1.text, self.board.food_id, self.board.snake2.parts)
            self.board.snake1.set_direction()

        self.board.snake1.move()

        # Second snake's move
        if self.board.snake2.is_dead(self.board.snake1.parts):
            self.lbl_status.text = 'GAME OVER!'
            self.lbl_dead.prefix = 'Player 2'
            return

        if self.cbb_mode_player2.text != 'Manual' and self.board.snake2.algorithm.food_id != self.board.food_id:
            self.board.snake2.find_path(self.cbb_mode_player2.text, self.board.food_id, self.board.snake1.parts)
        
        self.board.snake2.set_direction()
        if self.cbb_mode_player2.text != 'Manual' and self.board.snake2.is_near_dead(self.board.snake1.parts):
            self.board.snake2.find_path(self.cbb_mode_player2.text, self.board.food_id, self.board.snake1.parts)
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
        game.fps_controller.tick(FPS)

if __name__ == "__main__":
    main()