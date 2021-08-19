import csv
import hud
import mapa
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.keyboard import *
from PPlay.animation import *


class Game:
    def __init__(self, janela):
        self.janela = janela
        self.teclado = Keyboard()
        self.hud = hud.Hud(self.janela)

        # carrega o mapa
        self.mapa = mapa.Mapa(self.janela)

        # gameimages
        self.fundo = GameImage("assets/fundo_preto.png")

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

        self.velocidade = 400
        # self.player.stop()

        # posição relativa a tela
        self.player_frente.x = self.janela.width/2 - self.player.width
        self.player_frente.y = self.janela.height/2 - self.player.height
        self.player_costas.x = self.janela.width/2 - self.player.width
        self.player_costas.y = self.janela.height/2 - self.player.height
        self.player_esquerda.x = self.janela.width/2 - self.player.width
        self.player_esquerda.y = self.janela.height/2 - self.player.height
        self.player_direita.x = self.janela.width/2 - self.player.width
        self.player_direita.y = self.janela.height/2 - self.player.height

        self.mapa.carrega_mapa()

    def game_loop(self):
        while True:
            if self.teclado.key_pressed("ESC"):
                break

            if self.mapa.cim:
                self.player = self.player_costas
                self.player.update()
            if self.mapa.bai:
                self.player = self.player_frente
                self.player.update()
            if self.mapa.esq:
                self.player = self.player_esquerda
                self.player.update()
            if self.mapa.dir:
                self.player = self.player_direita
                self.player.update()
            self.player.play()

            self.mapa.move_player(self.player, self.velocidade)

            self.fundo.draw()

            self.mapa.desenha_layer(0)

            self.mapa.desenha_layer(1)

            self.player.draw()
            # if self.player.is_playing():
            #     if self.mapa.bai:
            #         self.player.update()
            #     if self.mapa.cim:
            #         self.player.update()

            self.mapa.desenha_layer(2)

            # desenha H.U.D.
            self.hud.draw_hud()

            self.janela.update()
