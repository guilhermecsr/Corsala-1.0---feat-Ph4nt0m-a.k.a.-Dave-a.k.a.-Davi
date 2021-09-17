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
import math

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
        self.objetos_info = [[[10, 10]], [[10, 3]], [[]]]
        self.objetos = [[], [], []]

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

    def move_player(self, player, velocidade):
        for i in range(len(self.mapa[var.MAPA_FLOOR])):
            for j in range(len(self.mapa[var.MAPA_FLOOR][i])):
                if var.BREAK:
                    var.BREAK = False
                    break
                if self.teclado.key_pressed("LEFT"):
                    if self.cim or self.bai:
                        var.PLAYER_VEL = var.PLAYER_VEL_ORIG*(math.sqrt(2)/2) + 50
                    else:
                        var.PLAYER_VEL = var.PLAYER_VEL_ORIG
                    self.esq = True
                    self.virado_esq = True
                    self.virado_dir = False
                    self.virado_cim = False
                    self.virado_bai = False
                    self.mapa[var.MAPA_FLOOR][i][j].x += velocidade * self.janela.delta_time()
                else:
                    self.esq = False

                if self.teclado.key_pressed("RIGHT"):
                    if self.cim or self.bai:
                        var.PLAYER_VEL = var.PLAYER_VEL_ORIG*(math.sqrt(2)/2) + 50
                    else:
                        var.PLAYER_VEL = var.PLAYER_VEL_ORIG
                    self.dir = True
                    self.virado_dir = True
                    self.virado_esq = False
                    self.virado_cim = False
                    self.virado_bai = False
                    self.mapa[var.MAPA_FLOOR][i][j].x -= velocidade * self.janela.delta_time()
                else:
                    self.dir = False

                if self.teclado.key_pressed("UP"):
                    if self.dir or self.esq:
                        var.PLAYER_VEL = var.PLAYER_VEL_ORIG*(math.sqrt(2)/2) + 50
                    else:
                        var.PLAYER_VEL = var.PLAYER_VEL_ORIG
                    self.cim = True
                    self.virado_cim = True
                    self.virado_dir = False
                    self.virado_esq = False
                    self.virado_bai = False
                    self.mapa[var.MAPA_FLOOR][i][j].y += velocidade * self.janela.delta_time()
                else:
                    self.cim = False

                if self.teclado.key_pressed("DOWN"):
                    if self.dir or self.esq:
                        var.PLAYER_VEL = var.PLAYER_VEL_ORIG*(math.sqrt(2)/2) + 50
                    else:
                        var.PLAYER_VEL = var.PLAYER_VEL_ORIG
                    self.bai = True
                    self.virado_bai = True
                    self.virado_dir = False
                    self.virado_cim = False
                    self.virado_esq = False
                    self.mapa[var.MAPA_FLOOR][i][j].y -= velocidade * self.janela.delta_time()
                else:
                    self.bai = False
                self.colisao(player, i, j, velocidade)

    def colisao(self, player, i, j, velocidade):
        if player.collided(self.mapa[var.MAPA_FLOOR][i][j]):
            aux = True
            if self.assets_especiais(self.mapa[var.MAPA_FLOOR][i][j], self.mapa[var.MAPA_FLOOR]):
                aux = False

            for k in range(len(self.mapa[var.MAPA_FLOOR])):
                if self.mapa[var.MAPA_FLOOR][i][j].solido:
                    for l in range(len(self.mapa[var.MAPA_FLOOR][k])):
                        if self.dir and aux:
                            self.mapa[var.MAPA_FLOOR][k][l].x += velocidade * self.janela.delta_time()

                        if self.esq and aux:
                            self.mapa[var.MAPA_FLOOR][k][l].x -= velocidade * self.janela.delta_time()

                        if self.cim and aux:
                            self.mapa[var.MAPA_FLOOR][k][l].y -= velocidade * self.janela.delta_time()

                        if self.bai and aux:
                            self.mapa[var.MAPA_FLOOR][k][l].y += velocidade * self.janela.delta_time()

    def assets_especiais(self, asset, mapa):
        array = []
        if asset.info:
            self.porta(asset)
            self.passagem(asset, mapa)
            self.passagem2(asset, mapa)
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
            elif array[4] == '2':
                var.BREAK = True
                var.MAPA_FLOOR = 2
                self.posix = int(''.join(array[0:2]))
                self.posiy = int(''.join(array[2:4]))
                self.reposiciona_assets(var.MAPA_FLOOR, self.posiy, self.posix)

    def porta(self, asset):
        if 'porta' in asset.info and asset.solido:
            self.janela.draw_text("*SPACE*", asset.x, asset.y, 20, (255, 255, 255))
            if self.teclado.key_pressed("space"):
                asset.set_curr_frame(1)
                asset.solido = False

    def passagem(self, asset, mapa):
        action = False
        if self.teclado.key_pressed("space"):
            action = True
        if 'puzzle1' in asset.info:
            if 'tocha' in asset.info:
                if not var.TOCHA:
                    self.janela.draw_text("Essa tocha esta meio torta...", asset.x, asset.y, 15, (255, 255, 255))
                if action:
                    var.TOCHA = True
                    asset.set_curr_frame(1)
                    mapa[10][4].set_curr_frame(1)
                    mapa[10][4].solido = False

            elif 'altar' in asset.info:
                if not action:
                    self.janela.draw_text("Por Deus, o que houve aqui?", asset.x, asset.y, 15, (255, 255, 255))
                elif action and var.ORACLE:
                    self.janela.draw_text("Sangue é vida, eu acho...", asset.x, asset.y, 15, (255, 255, 255))
                    var.ALTAR = True

            elif 'oracle' in asset.info:
                if not action:
                    self.janela.draw_text("'Ponha vida em minhas mãos que lhe mostrarei o caminho' hum...", asset.x, asset.y, 15, (255, 255, 255))
                    var.ORACLE = True
                elif action and var.ALTAR:
                    self.janela.draw_text("Sangue é vida, eu acho...", asset.x, asset.y, 15, (255, 255, 255))
                    var.PUZZLE1 = True
                    porta = Sprite('assets/96x96/porta_madeira_ch4.png', True, 2, 'porta')
                    porta.x = mapa[12][15].x
                    porta.y = mapa[12][15].y
                    mapa[12][15] = porta
                    mapa[12][15].set_total_duration(1000)
                    self.janela.draw_text("*Click*", self.janela.width/2, self.janela.height-100, 15, (255, 255, 255))

    def passagem2(self, asset, mapa):
        action = False
        if self.teclado.key_pressed("space"):
            action = True

        if 'puzzle2' in asset.info:
            if 'machine' in asset.info:
                if not var.CRYSTAL:
                    self.janela.draw_text("Uma invenção galvânica, parece sem energia...", asset.x, asset.y, 15, (255, 255, 255))
                elif var.CRYSTAL and action:
                    var.MACHINE = True
                    self.janela.draw_text("Melhor não tocar nisso...", asset.x, asset.y, 15, (255, 255, 255))
                if var.MACHINE:
                    var.PUZZLE2 = True
                    for i in range(1, 7):
                        exec(f"self.teleport_machine_{i}.set_curr_frame(1)")

            elif 'crystal' in asset.info:
                if not action and not var.CRYSTAL:
                    self.janela.draw_text("Ah, esse tipo de cristal não é dessa região...", asset.x, asset.y, 15,
                                          (255, 255, 255))
                else:
                    asset.set_curr_frame(1)
                    self.janela.draw_text("*Peguei*", asset.x, asset.y, 15, (255, 255, 255))
                    var.CRYSTAL = True

            if var.PUZZLE2:
                mapa[13][1].set_curr_frame(1)
                mapa[13][1].info = '25072'

    def desenha_layer(self):
        for i in range(len(self.mapa[var.MAPA_FLOOR])):
            for j in range(len(self.mapa[var.MAPA_FLOOR][i])):
                self.mapa[var.MAPA_FLOOR][i][j].draw()
                # pass
                # self.janela.draw_text("({}, {})".format(j, i),
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
    def carrega_mapa(self, mapa, posiy=17, posix=11):
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

                elif 'porta' in mapa[i][j]:
                    exec(f"self.{mapa[i][j]} = Sprite('assets/96x96/{mapa[i][j]}.png', True, 2, '{mapa[i][j]}')")
                    exec(f"self.{mapa[i][j]}.set_total_duration(1000)")
                    exec(f"self.{mapa[i][j]}.play()")
                    mapa[i][j] = eval(f"self.{mapa[i][j]}")

                elif 'machine' in mapa[i][j]:
                    exec(f"self.{mapa[i][j]} = Sprite('assets/96x96/{mapa[i][j]}.png', True, 2, info='puzzle2 machine')")
                    exec(f"self.{mapa[i][j]}.set_total_duration(1000)")
                    exec(f"self.{mapa[i][j]}.play()")
                    mapa[i][j] = eval(f"self.{mapa[i][j]}")

                elif 'escada' in mapa[i][j]:
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

                else:
                    self.pilar_baixo_largo = Sprite("assets/96x96/pilar_baixo_largo.png", True)
                    self.void = Sprite("assets/96x96/void.png", False)
                    self.tocha_par_hor = Sprite("assets/96x96/tocha_par_hor.png", True)
                    self.tocha_par_hor_torta = Sprite("assets/96x96/tocha_par_hor_torta.png", True, 2, info='puzzle1 tocha')
                    self.passagem_secreta_1 = Sprite("assets/96x96/passagem_secreta.png", True, 2, info='puzzle1 passagem')
                    self.altar_sangue_1 = Sprite("assets/96x96/altar_sangue_1.png", True, info='puzzle1 altar')
                    self.altar_sangue_2 = Sprite("assets/96x96/altar_sangue_2.png", True, info='puzzle1 altar')
                    self.the_oracle = Sprite("assets/96x96/the_oracle.png", True, info='puzzle1 oracle')
                    self.teleport_crystal_ch4 = Sprite("assets/96x96/teleport_crystal_ch4.png", False, 2, info='puzzle2 crystal')
                    self.teleport_ch4 = Sprite("assets/96x96/teleport_ch4.png", False, 2, info='puzzle2 tp')
                    self.cama_ch5_1 = Sprite("assets/96x96/cama_ch5_1.png", True)
                    self.cama_ch5_2 = Sprite("assets/96x96/cama_ch5_2.png", True)

                    mapa[i][j] = eval(f"self.{mapa[i][j]}")

                # loanding
                self.loading += 1
               # print("{}%".format(self.loading/4))

                mapa[i][j].x = j * 96 - (posix * 96 - self.janela.width/2)
                mapa[i][j].y = i * 96 - (posiy * 96 - self.janela.height/2)
        return mapa

    def reposiciona_assets(self, floor, posiy, posix):
        for i in range(len(self.mapa[floor])):
            for j in range(len(self.mapa[floor][i])):
                self.mapa[floor][i][j].x = j * 96 - (posiy * 96 - self.janela.width / 2)
                self.mapa[floor][i][j].y = i * 96 - (posix * 96 - self.janela.height / 2)
