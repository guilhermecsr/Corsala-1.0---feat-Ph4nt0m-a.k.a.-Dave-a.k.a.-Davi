from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.gameimage import *
from jogo import *
from mapa import *


class Menu:
    def __init__(self, janela, fundo, jogo):
        self.janela = janela
        self.fundo = fundo
        self.jogo = jogo
        self.mapa = Mapa(self.janela)
        self.mouse = Mouse()
        self.mouse.hide()
        self.counter = 0

        # assets
        self.button = Sprite("assets/Start_button1.png")
        self.button_start = Sprite("assets/Start_button1.png")
        self.button_exit = Sprite("assets/Exit_button1.png")
        self.cursor = Sprite("assets/dwarven_gauntlet.png")

        # assets position
        self.menu_x = janela.width / 2 - self.button.width / 2
        self.menu_y = janela.height / 2 - self.button.height / 2

        self.button_start.x = self.menu_x
        self.button_start.y = self.menu_y

        self.button_exit.x = self.menu_x
        self.button_exit.y = self.menu_y + self.button.height + 25

    def menu_loop(self):
        while True:
            # cursor
            self.cursor.x, self.cursor.y = self.mouse.get_position()[0], self.mouse.get_position()[1]

            # cliques
            if self.mouse.is_over_object(self.button_exit) and self.mouse.is_button_pressed(1):
                break

            self.button_start = Sprite("assets/start_button.png", False, 2)
            self.button_start.set_sequence(0, 1)
            self.button_start.x = self.janela.width / 2 - self.button.width / 2
            self.button_start.y = self.janela.height / 2 - self.button.height / 2

            self.button_exit = Sprite("assets/exit_button.png", False, 2)
            self.button_exit.set_sequence(0, 1)
            self.button_exit.x = self.menu_x
            self.button_exit.y = self.menu_y + self.button.height + 25

            if self.mouse.is_over_object(self.button_start):
                self.button_start.set_curr_frame(1)

            if self.mouse.is_over_object(self.button_start) and self.mouse.is_button_pressed(1):
                self.jogo.game_loop()

            if self.mouse.is_over_object(self.button_exit):
                self.button_exit.set_curr_frame(1)

            self.fundo.draw()
            self.button_start.draw()
            self.button_exit.draw()
            self.cursor.draw()
            self.janela.draw_text(f'pos : {self.mouse.get_position()}', 15, 15, size=20, color=(100, 100, 0))
            self.janela.update()
