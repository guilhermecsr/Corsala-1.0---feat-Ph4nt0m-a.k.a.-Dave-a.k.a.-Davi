from inimigos import *
from PPlay.keyboard import *


class Combate:
    def __init__(self, janela, player):
        self.janela = janela
        self.player = player.player
        self.inimigos = inimigos
        self.teclado = Keyboard

        self.sword_frente = Sprite("assets/jogador/sword_frente.png", False, 4)
        self.sword_frente.set_sequence_time(0, 3, 250)
        self.sword_costas = Sprite("assets/jogador/sword_costas.png", False, 4)
        self.sword_costas.set_sequence_time(0, 3, 250)
        self.sword_direita = Sprite("assets/jogador/sword_direita.png", False, 4)
        self.sword_direita.set_sequence_time(0, 3, 250)
        self.sword_esquerda = Sprite("assets/jogador/sword_esquerda.png", False, 4)
        self.sword_esquerda.set_sequence_time(0, 3, 250)
        self.sword = self.sword_frente
        self.sword.x = self.player.x - self.player.width / 2
        self.sword.y = self.player.y + self.player.height

        self.cooldown = 0

    def atack(self, cima, baixo, esquerda, direita, ataque=False):
        self.cim = cima
        self.bai = baixo
        self.esq = esquerda
        self.dir = direita
        if self.cim:
            self.sword = self.sword_costas
            self.sword.update()
            self.sword.x = self.player.x - self.player.width/2
            self.sword.y = self.player.y - self.player.height
        if self.bai:
            self.sword = self.sword_frente
            self.sword.update()
            self.sword.x = self.player.x - self.player.width/2
            self.sword.y = self.player.y + self.player.height
        if self.esq:
            self.sword = self.sword_esquerda
            self.sword.update()
            self.sword.x = self.player.x - self.sword.width
            self.sword.y = self.player.y
        if self.dir:
            self.sword = self.sword_direita
            self.sword.update()
            self.sword.x = self.player.x + self.player.width
            self.sword.y = self.player.y
        self.sword.play()
        self.sword.update()

    def acerto(self, mobs, info_mobs, cooldown):
        self.cooldown = cooldown
        acerto = False
        if self.cooldown >= 1:
            for i in range(len(mobs)):
                if info_mobs[i][2] > 0 and info_mobs[i][4] == var.MAPA_FLOOR:
                    if self.sword.collided(mobs[i][info_mobs[i][3]]):
                        acerto = True
                        info_mobs[i][2] -= 1
        self.sword.draw()
        return acerto

    def desenha_ataque(self):
        self.sword.draw()
