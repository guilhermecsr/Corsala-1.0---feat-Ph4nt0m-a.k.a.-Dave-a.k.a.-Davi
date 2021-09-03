import csv
import inimigos
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.keyboard import *
from os import listdir
from os.path import isfile, join
from inimigos import *

class Mapa:
    def __init__(self, janela):
        self.janela = janela
        self.teclado = Keyboard()
        self.inimigos = inimigos.Inimigos

        # carrega o mapa
        self.zero = open('maps/0.csv')
        self.um = open('maps/1.csv')
        # self.dois = open('maps/2.csv')
        self.reader = csv.reader(self.zero)
        self.aviso_de_comandos = Sprite("assets/aviso_de_comandos.png", False, 1)
        self.mapa = []
        self.chao = self
        self.parede = self
        self.floor = 0

        self.assets_array = [f for f in listdir("assets/96x96") if isfile(join("assets/96x96", f))]

        self.dir = False
        self.esq = False
        self.cim = False
        self.bai = False
        self.virado_dir = False
        self.virado_esq = False
        self.virado_cim = False
        self.virado_bai = False
        self.posix = 9
        self.posiy = 15

        # loanding
        self.loading = 0

    # TODO: acertar a movimentacao do mapa quando encostar em assets especiais
    def move_player(self, player, velocidade):
        self.velocidade = velocidade
        for i in range(len(self.mapa[self.floor])):
            for j in range(len(self.mapa[self.floor][i])):
                if self.teclado.key_pressed("LEFT"):
                    self.esq = True
                    self.virado_esq = True
                    self.virado_dir = False
                    self.virado_cim = False
                    self.virado_bai = False
                    self.mapa[self.floor][i][j].x += self.velocidade * self.janela.delta_time()
                else:
                    self.esq = False

                if self.teclado.key_pressed("RIGHT"):
                    self.dir = True
                    self.virado_dir = True
                    self.virado_esq = False
                    self.virado_cim = False
                    self.virado_bai = False
                    self.mapa[self.floor][i][j].x -= self.velocidade * self.janela.delta_time()
                else:
                    self.dir = False

                if self.teclado.key_pressed("UP"):
                    self.cim = True
                    self.virado_cim = True
                    self.virado_dir = False
                    self.virado_esq = False
                    self.virado_bai = False
                    self.mapa[self.floor][i][j].y += self.velocidade * self.janela.delta_time()
                else:
                    self.cim = False

                if self.teclado.key_pressed("DOWN"):
                    self.bai = True
                    self.virado_bai = True
                    self.virado_dir = False
                    self.virado_cim = False
                    self.virado_esq = False
                    self.mapa[self.floor][i][j].y -= self.velocidade * self.janela.delta_time()
                else:
                    self.bai = False
                self.colisao(player, i, j)

    def colisao(self, player, i, j):
        if player.collided(self.mapa[self.floor][i][j]):
            aux = True
            if self.assets_especiais(self.mapa[self.floor][i][j]):  aux = False

            # print(self.floor)
            for k in range(len(self.mapa[self.floor])):
                if self.mapa[self.floor][i][j].solido:
                    for l in range(len(self.mapa[self.floor][k])):
                        if self.dir and aux == True:
                            self.mapa[self.floor][k][l].x += self.velocidade * self.janela.delta_time()

                        if self.esq and aux == True:
                            self.mapa[self.floor][k][l].x -= self.velocidade * self.janela.delta_time()

                        if self.cim and aux == True:
                            self.mapa[self.floor][k][l].y -= self.velocidade * self.janela.delta_time()

                        if self.bai and aux == True:
                            self.mapa[self.floor][k][l].y += self.velocidade * self.janela.delta_time()

    def assets_especiais(self, asset):
        array = []
        if asset.info:
            for i in asset.info:
                array.append(i)
            if array[4] == '0':
                self.floor = 0
                self.posix = int(''.join(array[0:2]))
                self.posiy = int(''.join(array[2:4]))
                #self.carrega_mapa(self.posix, self.posiy)
            elif array[4] == '1':
                self.floor = 1
                self.posix = int(''.join(array[0:2]))
                self.posiy = int(''.join(array[2:4]))
                # self.carrega_mapa(self.posix, self.posiy)

    def desenha_layer(self):
        for i in range(len(self.mapa[self.floor])):
            for j in range(len(self.mapa[self.floor][i])):
                self.mapa[self.floor][i][j].draw()
                # self.janela.draw_text("({}, {})".format(i, j),
                #                       self.mapa[self.floor][i][j].x + 10,
                #                       self.mapa[self.floor][i][j].y,
                #                       12,
                #                       (255, 255, 255))

    def aloca_mapa(self, x=17, y=11):
        for i in range(2):
            if i == 0:
                reader = csv.reader(self.zero)
            elif i == 1:
                reader = csv.reader(self.um)
            self.mapa.append(list())
            for linha in reader:
                self.mapa[i].append(linha[:])
            self.carrega_mapa(self.mapa[i], x, y)
        return self.mapa

    # rever a volta da escada
    def carrega_mapa(self, mapa, posix=17, posiy=11):
        self.loading = 0
        self.loading = 0

        for i in range(len(mapa)):
            for j in range(len(mapa[i])):

                if 'parede' in mapa[i][j] or 'estrutura' in mapa[i][j]:
                    exec(f"self.{mapa[i][j]} = Sprite('assets/96x96/{mapa[i][j]}.png', True)")
                    mapa[i][j] = eval(f"self.{mapa[i][j]}")
                elif 'chao' in mapa[i][j] or 'bueiro' in mapa[i][j]:
                    exec(f"self.{mapa[i][j]} = Sprite('assets/96x96/{mapa[i][j]}.png', False)")
                    mapa[i][j] = eval(f"self.{mapa[i][j]}")
                else:
                    self.pilar_baixo_largo = Sprite("assets/96x96/pilar_baixo_largo.png", True)
                    self.void = Sprite("assets/96x96/void.png", False)
                    self.escada = Sprite("assets/96x96/escada.png", False)
                    self.escada_dupla_subir_1 = Sprite("assets/96x96/escada_dupla_subir_1.png", True)
                    self.escada_dupla_subir_2 = Sprite("assets/96x96/escada_dupla_subir_2.png", True)
                    self.escada_dupla_subir_3 = Sprite("assets/96x96/escada_dupla_subir_3.png", False, info='05101')
                    self.escada_dupla_subir_4 = Sprite("assets/96x96/escada_dupla_subir_4.png", False, info='05111')
                    self.escada_dupla_subir_5 = Sprite("assets/96x96/escada_dupla_subir_5.png", False)
                    self.escada_dupla_subir_6 = Sprite("assets/96x96/escada_dupla_subir_6.png", False)
                    self.escada_dupla_descer_1 = Sprite("assets/96x96/escada_dupla_descer_1.png", True)
                    self.escada_dupla_descer_2 = Sprite("assets/96x96/escada_dupla_descer_2.png", True)
                    self.escada_dupla_descer_3 = Sprite("assets/96x96/escada_dupla_descer_3.png", False, info='05040')
                    self.escada_dupla_descer_4 = Sprite("assets/96x96/escada_dupla_descer_4.png", False, info='05050')
                    self.escada_dupla_descer_5 = Sprite("assets/96x96/escada_dupla_descer_5.png", False)
                    self.escada_dupla_descer_6 = Sprite("assets/96x96/escada_dupla_descer_6.png", False)

                    mapa[i][j] = eval(f"self.{mapa[i][j]}")

                # loanding
                self.loading += 1

               # print("{}%".format(self.loading/4))

                mapa[i][j].x = j * 96 - (posiy * 96 - self.janela.width/2)
                mapa[i][j].y = i * 96 - (posix * 96 - self.janela.height/2)
        return mapa
