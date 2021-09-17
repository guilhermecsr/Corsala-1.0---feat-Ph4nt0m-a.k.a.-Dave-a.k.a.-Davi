from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.gameimage import *
from PPlay.keyboard import *
from jogo import *
from mapa import *


class Menu:
    def __init__(self, janela, fundo, jogo):
        self.janela = janela
        self.fundo = fundo
        self.jogo = jogo
        self.mapa = Mapa(self.janela)
        self.mouse = Mouse()
        self.teclado = Keyboard()
        self.mouse.hide()
        self.counter = 0
        self.direx = 1
        self.direy = 1
        self.counter = 0

        # assets
        self.button = Sprite("assets/start_button.png", False, 2)
        self.titulo = Sprite("assets/titulo_corsala.png")
        self.cursor = Sprite("assets/dwarven_gauntlet.png")
        self.button_start = Sprite("assets/start_button.png", False, 2)
        self.button_start.set_sequence(0, 1)
        self.button_exit = Sprite("assets/exit_button.png", False, 2)
        self.button_exit.set_sequence(0, 1)


        # assets position
        self.menu_x = janela.width / 2 - self.button.width / 2
        self.menu_y = janela.height / 2 - self.button.height / 2

        self.titulo.x = self.janela.width / 2 - self.titulo.width / 2
        self.titulo.y = self.janela.height / 2 - self.titulo.height / 2

        self.button_start.x = self.menu_x
        self.button_start.y = self.menu_y

        self.button_exit.x = self.menu_x
        self.button_exit.y = self.menu_y + self.button.height + 25

    def move_fundo(self):
        if abs(self.fundo.x) >= (self.janela.width) or self.fundo.x >= 0:
            self.direx *= -1
        self.fundo.x -= 20 * self.direx * self.janela.delta_time()

        if abs(self.fundo.y) >= (self.janela.height) or self.fundo.y >= 0:
            self.direy *= -1
        self.fundo.y -= 40 * self.direy * self.janela.delta_time()

    def menu_loop(self):

        while True:
            self.counter += self.janela.delta_time()

            # cursor
            self.cursor.x, self.cursor.y = self.mouse.get_position()[0], self.mouse.get_position()[1]

            # cliques

            if self.mouse.is_over_object(self.button_start) and self.mouse.is_button_pressed(1) and self.counter >= 0.5:
                self.counter = 0
                self.jogo.game_loop()

            if self.mouse.is_over_object(self.button_exit) and self.mouse.is_button_pressed(1) and self.counter >= 0.5:
                self.counter = 0
                break

            if self.mouse.is_over_object(self.button_start):
                self.button_start.set_curr_frame(1)
            else:
                self.button_start.set_curr_frame(0)

            if self.mouse.is_over_object(self.button_exit):
                self.button_exit.set_curr_frame(1)
            else:
                self.button_exit.set_curr_frame(0)

            self.fundo.draw()
            self.move_fundo()
            self.button_start.draw()
            self.button_exit.draw()
            self.titulo.draw()
            self.cursor.draw()
            self.janela.draw_text(f'pos : {self.mouse.get_position()}', 15, 15, size=20, color=(100, 100, 0))
            self.janela.update()
