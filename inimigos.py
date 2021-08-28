import jogo
import mapa
from PPlay.sprite import *
import hud
# from jogo import *
from mapa import *
import math


class Inimigos:
    def __init__(self, janela, jogo, player):
        self.janela = janela
        self.jogo = jogo
        self.hud = hud
        self.mobs = []
        self.mapa = mapa.Mapa
        self.player = player

        self.soldado_frente = Sprite("assets/mobs/soldado_frente.png", False, 0, 3)
        self.soldado_costas = Sprite("assets/mobs/soldado_costas.png", False, 0, 3)
        self.soldado_direita = Sprite("assets/mobs/soldado_direita.png", False, 0, 3)
        self.soldado_esquerda = Sprite("assets/mobs/soldado_esquerda.png", False, 0, 3)
        self.soldado = self.soldado_frente

        self.coordenadas = [[15, 15], [3, 3], [3, 5]]
        self.ref = []
        self.a = 0
        self.b = 0

        self.visap_mob = 400

        self.cooldown = 0

    def coordenadas_mobs(self):
        return self.coordenadas

    def get_line(self, start, end):
        # """Bresenham's Line Algorithm
        # Produces a list of tuples from start and end
        #
        # >>> points1 = self.get_line((0, 0), (3, 4))
        # >>> points2 = self.get_line((3, 4), (0, 0))
        # >>> assert(set(points1) == set(points2))
        # >>> print points1
        # [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
        # >>> print points2
        # [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
        # """
        # Setup initial conditions
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1

        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)

        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Swap start and end points if necessary and store swap state
        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True

        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1

        # Calculate error
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1

        # Iterate over bounding box generating points between start and end
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

        # Reverse the list if the coordinates were swapped
        if swapped:
            points.reverse()
        return points

    def visao(self, i):
        soldado_x = self.mobs[i].x + self.mobs[i].width/2
        soldado_y = self.mobs[i].y + self.mobs[i].height/2
        player_x = self.player.x + self.player.width/2
        player_y = self.player.y + self.player.height/2
        dist = (abs(soldado_x - player_x) + abs(soldado_y - player_y))
        if dist <= self.visap_mob:
            self.visap_mob = 800
            return True
        self.visap_mob = 400
        return False

    '''the range_ argument represents the maximum shooting distance at which the shooter will start firing.
        and obstacles is a list of obstacles, shooter and target are both pygame Sprites'''

    def visao_em_linha(self, shooter, target, range_, obstacles, i):
        if self.visao(i):
            line_of_sight = self.get_line(shooter.rect.center, target.rect.center)
            zone = shooter.rect.inflate(range_, range_)
            obstacles_list = [rectangle.rect for rectangle in obstacles]  # to support indexing
            obstacles_in_sight = zone.collidelistall(obstacles_list)
            for x in range(1, len(line_of_sight), 5):
                for obs_index in obstacles_in_sight:
                    if obstacles_list[obs_index].collidepoint(line_of_sight[x]):
                        return False
            return True

    def cria_mobs(self):
        for i in self.coordenadas:
            self.soldado = Sprite("assets/mobs/soldado_frente.png", False, 0, 3, "monstro", 5)
            self.mobs.append(self.soldado)
            self.ref.append([self.a, self.b])
        return self.mobs

    def movimenta_mobs(self, mapa, hit=False):
        obstaculos = []
        for i in range(len(mapa)):
            for j in range(len(mapa[i])):
                if mapa[i][j].solido:
                    obstaculos.append(mapa[i][j])

        for i in range(len(self.mobs)):
            if hit:
                h = -10
            else:
                h = 1
            if self.visao_em_linha(self.player, self.mobs[i], 800, obstaculos, i):
                if self.mobs[i].x + self.mobs[i].width/2 < self.player.x:
                    self.ref[i][0] += 200 * self.janela.delta_time() * h

                elif self.mobs[i].x + self.mobs[i].width/2 > self.player.x + self.player.width:
                    self.ref[i][0] -= 200 * self.janela.delta_time() * h

                elif self.mobs[i].y + self.mobs[i].height/2 < self.player.y:
                    self.ref[i][1] += 200 * self.janela.delta_time() * h

                elif self.mobs[i].y + self.mobs[i].height/2 > self.player.y + self.player.height:
                    self.ref[i][1] -= 200 * self.janela.delta_time() * h
            self.mobs[i].x = mapa[self.coordenadas[i][0]][self.coordenadas[i][1]].x + self.ref[i][0]
            self.mobs[i].y = mapa[self.coordenadas[i][0]][self.coordenadas[i][1]].y + self.ref[i][1]

    def dano(self, player_hp):
        self.cooldown += self.janela.delta_time()
        for i in range(len(self.mobs)):
            if self.janela.width/2 - 500 < self.mobs[i].\
                    x < self.janela.width/2 + 500 and self.janela.height/2 - 500 < self.mobs[i].\
                    y < self.janela.height/2 + 500 and self.cooldown >= 1:
                if self.mobs[i].collided(self.player) and player_hp > 0:
                    player_hp -= 1
                    self.cooldown = 0
                    self.hud.hp = player_hp
        return player_hp

    def desenha_inimigos(self):
        for i in range(len(self.mobs)):
            self.mobs[i].draw()
            self.janela.draw_text("{}{}{}{}{}".format('*' if self.mobs[i].health == 5 else "-",
                                                  '*' if self.mobs[i].health >= 4 else "-",
                                                  '*' if self.mobs[i].health >= 3 else "-",
                                                  '*' if self.mobs[i].health >= 2 else "-",
                                                  '*' if self.mobs[i].health >= 1 else "-"),
                                  self.mobs[i].x + 5,
                                  self.mobs[i].y - 10,
                                  20,
                                  (255, 255, 255))
