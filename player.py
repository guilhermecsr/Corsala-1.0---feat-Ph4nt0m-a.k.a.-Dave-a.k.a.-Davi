import inimigos
from PPlay.sprite import *
from PPlay.keyboard import *
from PPlay.gameimage import *
import variaveis as var
import sys


class Player:
    def __init__(self, janela):
        self.janela = janela
        self.teclado = Keyboard()
        self.game_over = GameImage("assets/game_over.jpg")

        # player
        self.player_frente = Sprite("assets/jogador/player_frente.png", True, 3)
        self.player_frente.set_sequence_time(0, 2, 100)
        self.player_costas = Sprite("assets/jogador/player_costas.png", True, 3)
        self.player_costas.set_sequence_time(0, 2, 100)
        self.player_direita = Sprite("assets/jogador/player_direita.png", True, 3)
        self.player_direita.set_sequence_time(0, 2, 100)
        self.player_esquerda = Sprite("assets/jogador/player_esquerda.png", True, 3)
        self.player_esquerda.set_sequence_time(0, 2, 100)
        self.player = self.player_frente

        self.sangue = Sprite("assets/jogador/sangue.png")
        self.sangue.x = self.janela.width / 2 - self.sangue.width
        self.sangue.y = self.janela.height / 2 - self.sangue.height - 20
        self.sangue.set_total_duration(500)
        self.sangue.play()
        self.sangue_count = 0

        self.sword_frente = Sprite("assets/jogador/sword_frente.png", False, 4)
        self.sword_frente.set_sequence_time(0, 3, 250)
        self.sword_costas = Sprite("assets/jogador/sword_costas.png", False, 4)
        self.sword_costas.set_sequence_time(0, 3, 250)
        self.sword_direita = Sprite("assets/jogador/sword_direita.png", False, 4)
        self.sword_direita.set_sequence_time(0, 3, 250)
        self.sword_esquerda = Sprite("assets/jogador/sword_esquerda.png", False, 4)
        self.sword_esquerda.set_sequence_time(0, 3, 250)
        self.sword = self.sword_frente

        self.velocidade = var.PLAYER_VEL
        # self.player.stop()

        # posição relativa a tela
        self.player_frente.x = self.janela.width / 2 - self.player.width
        self.player_frente.y = self.janela.height / 2 - self.player.height
        self.player_costas.x = self.janela.width / 2 - self.player.width
        self.player_costas.y = self.janela.height / 2 - self.player.height
        self.player_esquerda.x = self.janela.width / 2 - self.player.width
        self.player_esquerda.y = self.janela.height / 2 - self.player.height
        self.player_direita.x = self.janela.width / 2 - self.player.width
        self.player_direita.y = self.janela.height / 2 - self.player.height

        # atributos
        self.player_hp = 10

    def move_player(self):
        if self.teclado.key_pressed("UP"):
            self.player = self.player_costas
            self.player.update()
        if self.teclado.key_pressed("DOWN"):
            self.player = self.player_frente
            self.player.update()
        if self.teclado.key_pressed("LEFT"):
            self.player = self.player_esquerda
            self.player.update()
        if self.teclado.key_pressed("RIGHT"):
            self.player = self.player_direita
            self.player.update()
        self.player.play()

    def player_toma_dano(self):
        if var.PLAYER_HIT:
            self.sangue_count += self.janela.delta_time()
            self.sangue.draw()
            if self.sangue_count >= 0.1:
                self.sangue_count = 0
                var.PLAYER_HIT = False


    def mata_player(self, mobs, hp):
        if hp <= 0:
            self.fim(mobs)

    def fim(self, mobs):
        mobs.clear()
        while True:
            self.game_over.draw()
            if self.teclado.key_pressed("ESC"):
                sys.exit()
            self.janela.update()
