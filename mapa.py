import csv
import inimigos
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.keyboard import *
from os import listdir
from os.path import isfile, join
from inimigos import *
import variaveis as var
import os.path


class Mapa:
    def __init__(self, janela):
        self.janela = janela
        self.teclado = Keyboard()
        self.inimigos = inimigos.Inimigos

        # carrega o mapa
        self.zero = open('maps/0.csv')
        self.um = open('maps/1.csv')
        self.dois = open('maps/2.csv')
        self.reader = csv.reader(self.zero)
        self.aviso_de_comandos = Sprite("assets/aviso_de_comandos.png", False, 1)
        self.mapa = []
        self.chao = self
        self.parede = self
        var.MAPA_FLOOR = 0

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
        for i in range(len(self.mapa[var.MAPA_FLOOR])):
            for j in range(len(self.mapa[var.MAPA_FLOOR][i])):
                if self.teclado.key_pressed("LEFT"):
                    self.esq = True
                    self.virado_esq = True
                    self.virado_dir = False
                    self.virado_cim = False
                    self.virado_bai = False
                    self.mapa[var.MAPA_FLOOR][i][j].x += self.velocidade * self.janela.delta_time()
                else:
                    self.esq = False

                if self.teclado.key_pressed("RIGHT"):
                    self.dir = True
                    self.virado_dir = True
                    self.virado_esq = False
                    self.virado_cim = False
                    self.virado_bai = False
                    self.mapa[var.MAPA_FLOOR][i][j].x -= self.velocidade * self.janela.delta_time()
                else:
                    self.dir = False

                if self.teclado.key_pressed("UP"):
                    self.cim = True
                    self.virado_cim = True
                    self.virado_dir = False
                    self.virado_esq = False
                    self.virado_bai = False
                    self.mapa[var.MAPA_FLOOR][i][j].y += self.velocidade * self.janela.delta_time()
                else:
                    self.cim = False

                if self.teclado.key_pressed("DOWN"):
                    self.bai = True
                    self.virado_bai = True
                    self.virado_dir = False
                    self.virado_cim = False
                    self.virado_esq = False
                    self.mapa[var.MAPA_FLOOR][i][j].y -= self.velocidade * self.janela.delta_time()
                else:
                    self.bai = False
                self.colisao(player, i, j)

    def colisao(self, player, i, j):
        if player.collided(self.mapa[var.MAPA_FLOOR][i][j]):
            aux = True
            if self.assets_especiais(self.mapa[var.MAPA_FLOOR][i][j]):  aux = False

            # print(var.MAPA_FLOOR)
            for k in range(len(self.mapa[var.MAPA_FLOOR])):
                if self.mapa[var.MAPA_FLOOR][i][j].solido:
                    for l in range(len(self.mapa[var.MAPA_FLOOR][k])):
                        if self.dir and aux == True:
                            self.mapa[var.MAPA_FLOOR][k][l].x += self.velocidade * self.janela.delta_time()

                        if self.esq and aux == True:
                            self.mapa[var.MAPA_FLOOR][k][l].x -= self.velocidade * self.janela.delta_time()

                        if self.cim and aux == True:
                            self.mapa[var.MAPA_FLOOR][k][l].y -= self.velocidade * self.janela.delta_time()

                        if self.bai and aux == True:
                            self.mapa[var.MAPA_FLOOR][k][l].y += self.velocidade * self.janela.delta_time()

    def assets_especiais(self, asset):
        array = []
        if asset.info:
            for i in asset.info:
                array.append(i)
            if array[4] == '0':
                var.MAPA_FLOOR = 0
                self.posix = int(''.join(array[0:2]))
                self.posiy = int(''.join(array[2:4]))
                self.reposiciona_assets(var.MAPA_FLOOR, self.posiy, self.posix)
            elif array[4] == '1':
                var.MAPA_FLOOR = 1
                self.posix = int(''.join(array[0:2]))
                self.posiy = int(''.join(array[2:4]))
                self.reposiciona_assets(var.MAPA_FLOOR, self.posiy, self.posix)

    def desenha_layer(self):
        for i in range(len(self.mapa[var.MAPA_FLOOR])):
            for j in range(len(self.mapa[var.MAPA_FLOOR][i])):
                self.mapa[var.MAPA_FLOOR][i][j].draw()
                # self.janela.draw_text("({}, {})".format(i, j),
                #                       self.mapa[var.MAPA_FLOOR][i][j].x + 10,
                #                       self.mapa[var.MAPA_FLOOR][i][j].y,
                #                       12,
                #                       (255, 255, 255))

    def aloca_mapa(self, x=17, y=11):
        reader0 = csv.reader(self.zero)
        reader1 = csv.reader(self.um)
        reader2 = csv.reader(self.dois)
        self.mapa = [[], [], []]
        for linha in reader0:
            self.mapa[0].append(linha[:])
        for linha in reader1:
            self.mapa[1].append(linha[:])
        for linha in reader2:
            self.mapa[2].append(linha[:])
        self.mapa[0] = self.carrega_mapa(self.mapa[0], x, y)
        self.mapa[1] = self.carrega_mapa(self.mapa[1], x, y)
        self.mapa[2] = self.carrega_mapa(self.mapa[2], x, y)
        return self.mapa

    # rever a volta da escada
    def carrega_mapa(self, mapa, posix=17, posiy=11):
        self.loading = 0

        for i in range(len(mapa)):
            for j in range(len(mapa[i])):

                if 'parede' in mapa[i][j] or 'estrutura' in mapa[i][j]:
                    exec(f"self.{mapa[i][j]} = Sprite('assets/96x96/{mapa[i][j]}.png', True)")
                    mapa[i][j] = eval(f"self.{mapa[i][j]}")
                elif 'chao' in mapa[i][j] or 'bueiro' in mapa[i][j]:
                    exec(f"self.{mapa[i][j]} = Sprite('assets/96x96/{mapa[i][j]}.png', False)")
                    mapa[i][j] = eval(f"self.{mapa[i][j]}")
                elif 'jardim' in mapa[i][j]:
                    if os.path.exists(f'assets/jardim_solido/{mapa[i][j]}.jpg'):
                        exec(f"self.{mapa[i][j]} = Sprite('assets/jardim/{mapa[i][j]}.jpg', True)")
                    else:
                        exec(f"self.{mapa[i][j]} = Sprite('assets/jardim/{mapa[i][j]}.jpg', False)")
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

    def reposiciona_assets(self, floor, posiy, posix):
        for i in range(len(self.mapa[floor])):
            for j in range(len(self.mapa[floor][i])):
                self.mapa[floor][i][j].x = j * 96 - (posiy * 96 - self.janela.width / 2)
                self.mapa[floor][i][j].y = i * 96 - (posix * 96 - self.janela.height / 2)
