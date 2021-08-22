from PPlay.sprite import *
import jogo


class Inimigos:
    def __init__(self, janela, player, mapa):
        self.janela = janela
        self.player = player
        self.jogo = jogo
        self.mobs = []

        self.mapa = mapa
        self.soldado_frente = Sprite("assets/mobs/soldado_frente.png", False, 0, 3)
        self.soldado_costas = Sprite("assets/mobs/soldado_costas.png", False, 0, 3)
        self.soldado_direita = Sprite("assets/mobs/soldado_direita.png", False, 0, 3)
        self.soldado_esquerda = Sprite("assets/mobs/soldado_esquerda.png", False, 0, 3)
        self.soldado = self.soldado_frente

        self.coordenadas = [[18, 18]]
        self.a = 0
        self.b = 0

        # self.coordenada_y = []

    def visao(self):
        if 0 < self.soldado.x < self.janela.width and 0 < self.soldado.y < self.janela.height:
            return True
        return False

    def cria_mobs(self):
        self.soldado = Sprite("assets/mobs/soldado_frente.png", False, 0, 3)
        for i in self.coordenadas:
            self.soldado.x = self.mapa.mapa[i[0]][i[1]].x
            self.soldado.y = self.mapa.mapa[i[0]][i[1]].y
            self.mobs.append(self.soldado)


    def movimenta_mobs(self):
        for i in range(len(self.mobs)):
            self.mobs[i].x = self.mapa.mapa[self.coordenadas[i][0]][self.coordenadas[i][1]].x + self.a
            self.mobs[i].y = self.mapa.mapa[self.coordenadas[i][0]][self.coordenadas[i][1]].y + self.b
            if self.visao():
                if self.mobs[i].x + self.mobs[i].width/2 < self.player.x:
                    self.a += 200 * self.janela.delta_time()

                if self.mobs[i].x + self.mobs[i].width/2 > self.player.x + self.player.width:
                    self.a -= 200 * self.janela.delta_time()

                if self.mobs[i].y + self.mobs[i].height/2 < self.player.y:
                    self.b += 200 * self.janela.delta_time()

                if self.mobs[i].y + self.mobs[i].height/2 > self.player.y + self.player.height:
                    self.b -= 200 * self.janela.delta_time()


    def desenha_inimigos(self):
        for i in range(len(self.mobs)):
            self.mobs[i].draw()
            self.visao()
