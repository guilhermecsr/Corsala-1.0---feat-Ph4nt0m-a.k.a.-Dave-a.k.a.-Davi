import csv
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.keyboard import *


class Mapa:
    def __init__(self, janela):
        self.janela = janela
        self.teclado = Keyboard()

        # carrega o mapa
        self.ficheiro = open('maps/mapa_cela_teste.csv')
        self.reader = csv.reader(self.ficheiro)
        self.mapa = []
        self.mapaBaixo = []
        self.floor = []
        self.chao = self
        self.parede = self

        self.dir = False
        self.esq = False
        self.cim = False
        self.bai = False
        # pass

    def move_player(self, player):
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[i])):
                if self.teclado.key_pressed("LEFT"):
                    self.esq = True
                    self.mapa[i][j].x += 200 * self.janela.delta_time()
                else:
                    self.esq = False

                if self.teclado.key_pressed("RIGHT"):
                    self.dir = True
                    self.mapa[i][j].x -= 200 * self.janela.delta_time()
                else:
                    self.dir = False

                if self.teclado.key_pressed("UP"):
                    self.cim = True
                    self.mapa[i][j].y += 200 * self.janela.delta_time()
                else:
                    self.cim = False

                if self.teclado.key_pressed("DOWN"):
                    self.bai = True
                    self.mapa[i][j].y -= 200 * self.janela.delta_time()
                else:
                    self.bai = False
                self.colisao(player, i, j)

    def colisao(self, player, i, j):
        if player.collided(self.mapa[i][j]) and self.mapa[i][j].solido:
            for k in range(len(self.mapa)):
                for l in range(len(self.mapa[k])):
                    if self.dir:
                        self.mapa[k][l].x += 200 * self.janela.delta_time()

                    if self.esq:
                        self.mapa[k][l].x -= 200 * self.janela.delta_time()

                    if self.cim:
                        self.mapa[k][l].y -= 200 * self.janela.delta_time()

                    if self.bai:
                        self.mapa[k][l].y += 200 * self.janela.delta_time()

    def desenha_layer(self, layer):
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[i])):
                if self.mapa[i][j].layer == layer:
                    self.mapa[i][j].draw()

    def carrega_mapa(self):
        for linha in self.reader:
            self.mapa.append(linha[:])

        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[i])):
                self.pilar_baixo_largo = Sprite("assets/32x32/pilar_baixo_largo.png", True, 2)
                self.bueiro_c_agua = Sprite("assets/32x32/bueiro_c_agua.png", False, 1)
                self.bueiro_s_agua = Sprite("assets/32x32/bueiro_s_agua.png", False, 1)
                self.vazio = Sprite("assets/32x32/void.png", False, 0)
                self.chao1 = Sprite("assets/32x32/chao1.png", False, 1)
                self.chao2 = Sprite("assets/32x32/chao2.png", False, 1)
                self.chao3 = Sprite("assets/32x32/chao3.png", False, 1)
                self.chao4 = Sprite("assets/32x32/chao4.png", False, 1)
                self.chao5 = Sprite("assets/32x32/chao5.png", False, 1)
                self.chao6 = Sprite("assets/32x32/chao6.png", False, 1)
                self.chao7 = Sprite("assets/32x32/chao7.png", False, 1)
                self.escada = Sprite("assets/32x32/escada.png", False, 1)

                self.mapa[i][j] = eval("self.{}".format(self.mapa[i][j]))

                self.mapa[i][j].x = j * self.mapa[i][j].width
                self.mapa[i][j].y = i * self.mapa[i][j].height