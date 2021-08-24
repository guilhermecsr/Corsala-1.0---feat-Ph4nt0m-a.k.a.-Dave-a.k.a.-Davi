from PPlay.sprite import *
from PPlay.keyboard import *


class Player:
    def __init__(self, janela):
        self.janela = janela
        self.teclado = Keyboard()

        # player
        self.player_frente = Sprite("assets/jogador/player_frente.png", True, 0, 3)
        self.player_frente.set_sequence_time(0, 2, 100)
        self.player_costas = Sprite("assets/jogador/player_costas.png", True, 0, 3)
        self.player_costas.set_sequence_time(0, 2, 100)
        self.player_direita = Sprite("assets/jogador/player_direita.png", True, 0, 3)
        self.player_direita.set_sequence_time(0, 2, 100)
        self.player_esquerda = Sprite("assets/jogador/player_esquerda.png", True, 0, 3)
        self.player_esquerda.set_sequence_time(0, 2, 100)
        self.player = self.player_frente

        self.sword_frente = Sprite("assets/jogador/sword_frente.png", False, 0, 4)
        self.sword_frente.set_sequence_time(0, 3, 250)
        self.sword_costas = Sprite("assets/jogador/sword_costas.png", False, 0, 4)
        self.sword_costas.set_sequence_time(0, 3, 250)
        self.sword_direita = Sprite("assets/jogador/sword_direita.png", False, 0, 4)
        self.sword_direita.set_sequence_time(0, 3, 250)
        self.sword_esquerda = Sprite("assets/jogador/sword_esquerda.png", False, 0, 4)
        self.sword_esquerda.set_sequence_time(0, 3, 250)
        self.sword = self.sword_frente

        self.velocidade = 400
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

        # combate
        # self.combate = combate.Combate(janela, self.player)
        #
        # self.inimigos = inimigos.Inimigos(janela, self.player, self.mapa)

        # atributos
        self.player_hp = 10
        # self.hud = hud

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