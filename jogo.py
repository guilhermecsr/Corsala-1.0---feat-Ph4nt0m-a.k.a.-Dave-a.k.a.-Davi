import csv
import hud
import mapa
import combate
import inimigos
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
        self.mapa = mapa.Mapa(self.janela, inimigos)

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
        self.player_frente.x = self.janela.width/2 - self.player.width
        self.player_frente.y = self.janela.height/2 - self.player.height
        self.player_costas.x = self.janela.width/2 - self.player.width
        self.player_costas.y = self.janela.height/2 - self.player.height
        self.player_esquerda.x = self.janela.width/2 - self.player.width
        self.player_esquerda.y = self.janela.height/2 - self.player.height
        self.player_direita.x = self.janela.width/2 - self.player.width
        self.player_direita.y = self.janela.height/2 - self.player.height

        # combate
        self.combate = combate.Combate(janela, self.player)

        self.inimigos = inimigos.Inimigos(janela, self.player, self.mapa)

        self.mapa.carrega_mapa()
        self.inimigos.cria_mobs()

        # framerate
        self.fps = 0
        self.frames = 0
        self.relogio = 0

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

            self.inimigos.movimenta_mobs()

            self.player.draw()

            self.inimigos.desenha_inimigos()

            # carrega direcoes do player
            self.combate.atack(self.mapa.virado_cim, self.mapa.virado_bai, self.mapa.virado_esq, self.mapa.virado_dir, False)

            if self.teclado.key_pressed("SPACE"):
                for i in range(4):
                    self.combate.atack(self.mapa.cim, self.mapa.bai, self.mapa.esq, self.mapa.dir, True)
                    self.combate.desenha_ataque()

            self.mapa.desenha_layer(2)

            # desenha H.U.D.
            self.hud.draw_hud()

            # framerate
            if self.relogio >= 1:
                self.relogio = 0
                self.fps = self.frames
                self.frames = 0

            self.janela.draw_text("fps: {}".format(self.fps), 50, 10, 30, (255, 255, 255))
            self.relogio += self.janela.delta_time()
            self.frames += 1

            self.janela.update()
