import jogo
import mapa
import variaveis
from PPlay.sprite import *
import hud
# from jogo import *
from mapa import *
import math
import random as rd


class Inimigos:
    def __init__(self, janela, jogo, player):
        self.janela = janela
        self.jogo = jogo
        self.hud = hud
        self.mobs = []
        self.mapa = mapa.Mapa
        self.player = player

        # info_mobs -> [0=x, 1=y, 2=hp, 3=face, 4=floor, 5=hit, 6=mob]
        self.info_mobs = [[13, 14, 5, 0, 0, False, 'soldado_zumbi'],
                          [3, 2, 5, 0, 0, False, 'soldado_zumbi'],
                          [3, 5, 5, 0, 0, False, 'soldado_zumbi'],
                          [5, 4, 5, 0, 0, False, 'soldado_zumbi'],
                          [4, 1, 5, 0, 0, False, 'soldado_zumbi'],
                          [5, 2, 5, 0, 0, False, 'soldado_zumbi'],
                          [6, 3, 5, 0, 0, False, 'soldado_zumbi'],
                          [6, 1, 5, 0, 0, False, 'soldado_zumbi'],
                          [5, 6, 5, 0, 0, False, 'soldado_zumbi'],
                          [6, 5, 5, 0, 0, False, 'soldado_zumbi'],
                          [17, 4, 1, 0, 0, False, 'esqueleto', 0],
                          [9, 11, 1, 0, 2, False, 'esqueleto', 0],
                          [7, 9, 1, 0, 2, False, 'esqueleto', 0],
                          [8, 10, 15, 0, 2, False, 'necromancer']]
        # self.info_mobs_teaser = [[13, 12, 1, 0, 1, False, 'esqueleto'],
        #                   [14, 12, 1, 0, 1, False, 'esqueleto'],
        #                   [15, 12, 1, 0, 1, False, 'esqueleto'],
        #                   [16, 12, 1, 0, 1, False, 'esqueleto'],
        #                   [17, 12, 1, 0, 1, False, 'esqueleto'],
        #                   [18, 12, 1, 0, 1, False, 'esqueleto'],
        #                   [14, 13, 1, 0, 1, False, 'esqueleto'],
        #                   [15, 13, 1, 0, 1, False, 'esqueleto'],
        #                   [16, 13, 1, 0, 1, False, 'esqueleto'],
        #                   [17, 13, 1, 0, 1, False, 'esqueleto'],
        #                   [18, 13, 1, 0, 1, False, 'esqueleto'],
        #                   [15, 14, 1, 0, 1, False, 'esqueleto'],
        #                   [16, 14, 1, 0, 1, False, 'esqueleto'],
        #                   [17, 14, 1, 0, 1, False, 'esqueleto'],
        #                   [13, 13, 1, 0, 1, False, 'esqueleto'],
        #                   [14, 14, 1, 0, 1, False, 'esqueleto'],
        #                   [15, 15, 1, 0, 1, False, 'esqueleto'],
        #                   [16, 16, 1, 0, 1, False, 'esqueleto'],
        #                   [17, 17, 1, 0, 1, False, 'esqueleto'],
        #                   [18, 15, 1, 0, 1, False, 'esqueleto'],
        #                   [14, 15, 1, 0, 1, False, 'esqueleto'],
        #                   [14, 16, 1, 0, 1, False, 'esqueleto'],
        #                   [14, 17, 1, 0, 1, False, 'esqueleto'],
        #                   [15, 16, 1, 0, 1, False, 'esqueleto'],
        #                   [15, 17, 1, 0, 1, False, 'esqueleto'],
        #                   [17, 16, 1, 0, 1, False, 'esqueleto'],
        #                   [13, 16, 1, 0, 1, False, 'esqueleto'],
        #                   [13, 12, 1, 0, 1, False, 'esqueleto'],
        #                   [13, 13, 1, 0, 1, False, 'necromancer']]
        self.ref = []
        self.a = 0
        self.b = 0

        self.teleporte = Sprite("assets/mobs/teleport.png", frames=4)
        self.pixel = Sprite("assets/pixel.png")
        self.teleporte.set_total_duration(1500)
        self.teleporte.play()

        self.cooldown = 0
        self.skull_cooldown = 2

        self.skull_array = []

    def coordenadas_mobs(self):
        self.mata_mobs()
        return self.info_mobs

    def get_line(self, start, end):
        # Bresenham's Line Algorithm
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

    def visao(self, i, range_, face):
        mob1 = self.mobs[i][face]
        mob2 = self.player
        dist = self.distancia(mob1, mob2)
        if dist <= self.ref[i][2]:
            self.ref[i][2] = int(range_ * 1.5)
            return True
        self.ref[i][2] = range_
        return False

    def distancia(self, mob1, mob2):
        x1 = mob1.x - (mob1.width/2)
        y1 = mob1.y - (mob1.height/2)
        x2 = mob2.x - (mob2.width/2)
        y2 = mob2.y - (mob2.height/2)
        return abs(x1 - x2) + abs(y1 - y2)

    '''the range_ argument represents the maximum shooting distance at which the shooter will start firing.
        and obstacles is a list of obstacles, shooter and target are both pygame Sprites'''

    def visao_em_linha(self, shooter, target, range_, obstacles, i, face):
        visao = self.visao(i, range_, face)
        if visao:
            line_of_sight = self.get_line(shooter.rect.center, target.rect.center)
            # self.desenha_linha(line_of_sight)
            zone = shooter.rect.inflate(range_, range_)
            obstacles_list = [rectangle.rect for rectangle in obstacles]  # to support indexing
            obstacles_in_sight = zone.collidelistall(obstacles_list)
            for x in range(1, len(line_of_sight), 1):
                for obs_index in obstacles_in_sight:
                    if obstacles_list[obs_index].collidepoint(line_of_sight[x]):
                        return False
            return True

    def desenha_linha(self, line):
        for i in line:
            self.pixel.x, self.pixel.y = i
            self.pixel.draw()

    def cria_mobs(self):
        tipos = []
        for tipo in self.info_mobs:
            if tipo[6] not in tipos:
                tipos.append(tipo[6])
        frames = ['frente', 'esquerda', 'direita', 'costas']
        for info in range(len(self.info_mobs)):
            for mob in tipos:
                if self.info_mobs[info][6] == mob:
                    exec(f"self.{mob} = []")
                    for posi in frames:
                        exec(f"self.{mob}_{posi} = Sprite('assets/mobs/{mob}_{posi}.png', False, 3)")
                        exec(f"self.{mob}_{posi}.set_total_duration(1000)")
                        exec(f"self.{mob}_{posi}.play()")
                        exec(f"self.{mob}.append(self.{mob}_{posi})")
                    exec(f"self.{mob}_morto = Sprite('assets/mobs/{mob}_morto.png', False, 1)")
                    exec(f"self.{mob}_morto.x = 5000")
                    exec(f"self.{mob}.append(self.{mob}_morto)")
                    exec(f"self.mobs.append(self.{mob})")
                    self.ref.append([self.a, self.b, var.VISAO_MOB])
        return self.mobs

    def esqueleto_levanta(self, i):
        if 'esqueleto' in self.info_mobs[i][6]:
            if self.info_mobs[i][2] <= 0:
                self.info_mobs[i][7] += self.janela.delta_time()
                if self.info_mobs[i][7] >= 5:
                    self.info_mobs[i][2] = 1
                    self.info_mobs[i][7] = 0

    def movimenta_mobs(self, mapa):
        var.NECRO_TELEPORT += self.janela.delta_time()
        obstaculos = [[], [], []]
        for floor in range(2):
            for i in range(len(mapa[floor])):
                for j in range(len(mapa[floor][i])):
                    if mapa[floor][i][j].solido:
                        obstaculos[floor].append(mapa[floor][i][j])

        for i in range(len(self.mobs)):
            self.esqueleto_levanta(i)
            hp = self.info_mobs[i][2]
            face = self.info_mobs[i][3]
            andar = self.info_mobs[i][4]
            if not hp <= 0 and andar == var.MAPA_FLOOR:
                if self.info_mobs[i][5]:
                    h = -10
                    self.info_mobs[i][5] = False
                else:
                    h = 1
                if self.visao_em_linha(self.player,
                                       self.mobs[i][face],
                                       400, obstaculos[var.MAPA_FLOOR], i, face):
                    if 'necromancer' in self.info_mobs[i][6]:
                        self.info_mobs[i] = self.movimenta_mago(i, face, mapa[var.MAPA_FLOOR])
                        self.teleporte.x = self.mobs[i][face].x + (self.mobs[i][face].width/2) - (self.teleporte.width/2)
                        self.teleporte.y = self.mobs[i][face].y + self.mobs[i][face].height - self.teleporte.height
                    else:
                        if self.mobs[i][face].x + self.mobs[i][face].width/2 < self.player.x:
                            self.ref[i][0] += 200 * self.janela.delta_time() * h
                            self.info_mobs[i][3] = 2
                            self.mobs[i][2].update()

                        elif self.mobs[i][face].x + self.mobs[i][face].width/2 > self.player.x + self.player.width:
                            self.ref[i][0] -= 200 * self.janela.delta_time() * h
                            self.info_mobs[i][3] = 1
                            self.mobs[i][1].update()

                        elif self.mobs[i][face].y + self.mobs[i][face].height/2 < self.player.y:
                            self.ref[i][1] += 200 * self.janela.delta_time() * h
                            self.info_mobs[i][3] = 0
                            self.mobs[i][0].update()

                        elif self.mobs[i][face].y + self.mobs[i][face].height/2 > self.player.y + self.player.height:
                            self.ref[i][1] -= 200 * self.janela.delta_time() * h
                            self.info_mobs[i][3] = 3
                            self.mobs[i][3].update()
                self.mobs[i][self.info_mobs[i][3]].x = mapa[var.MAPA_FLOOR][self.info_mobs[i][0]][self.info_mobs[i][1]].x + self.ref[i][0]
                self.mobs[i][self.info_mobs[i][3]].y = mapa[var.MAPA_FLOOR][self.info_mobs[i][0]][self.info_mobs[i][1]].y + self.ref[i][1]
            else:
                if self.info_mobs[i][4] == var.MAPA_FLOOR:
                    self.mobs[i][self.info_mobs[i][3]].x = mapa[var.MAPA_FLOOR][self.info_mobs[i][0]][self.info_mobs[i][1]].x + self.ref[i][0]
                    self.mobs[i][self.info_mobs[i][3]].y = mapa[var.MAPA_FLOOR][self.info_mobs[i][0]][self.info_mobs[i][1]].y + self.ref[i][1]
                else:
                    continue

    def movimenta_mago(self, i, face, mapa):
        var.NECRODIST = (abs(self.mobs[i][face].x - self.player.x) + abs(self.mobs[i][face].y - self.player.y))
        if var.NECRODIST < 300:
            direcao = -1
        elif var.NECRODIST > 350:
            direcao = 1
        else:
            direcao = 0
        necro_vel = 200
        necro_vel = self.colisao_do_mago(self.mobs[i][face], mapa, necro_vel, i)

        self.info_mobs[i] = self.teleporte_mago(i, mapa)

        if self.mobs[i][face].x + self.mobs[i][face].width / 2 < self.player.x:
            self.ref[i][0] += necro_vel * self.janela.delta_time() * direcao
            self.info_mobs[i][3] = 2
            self.mobs[i][2].update()

        elif self.mobs[i][face].x + self.mobs[i][face].width / 2 > self.player.x + self.player.width:
            self.ref[i][0] -= necro_vel * self.janela.delta_time() * direcao
            self.info_mobs[i][3] = 1
            self.mobs[i][1].update()

        elif self.mobs[i][face].y + self.mobs[i][face].height / 2 < self.player.y:
            self.ref[i][1] += necro_vel * self.janela.delta_time() * direcao
            self.info_mobs[i][3] = 0
            self.mobs[i][0].update()

        elif self.mobs[i][face].y + self.mobs[i][face].height / 2 > self.player.y + self.player.height:
            self.ref[i][1] -= necro_vel * self.janela.delta_time() * direcao
            self.info_mobs[i][3] = 3
            self.mobs[i][3].update()
        return self.info_mobs[i]


    def colisao_do_mago(self, mago, mapa, vel, k):
        for i in range(len(mapa)):
            for j in range(len(mapa[i])):
                if mapa[i][j].solido:
                    if mago.collided(mapa[i][j]):
                        vel = 0
        return vel

    def teleporte_mago(self, k, mapa):
        if var.NECRODIST <= 100 and var.NECRO_TELEPORT >= 0.5:
            var.NECRO_TELEPORT = 0
            x = rd.randrange(2, len(mapa)-3)
            y = rd.randrange(2, len(mapa[x])-3)
            if not mapa[x][y].solido:
                self.info_mobs[k][0] = x
                self.info_mobs[k][1] = y

                self.teleporte.update()
                self.teleporte.draw()
        return self.info_mobs[k]

    def dano(self, player_hp):
        array = []
        self.cooldown += self.janela.delta_time()
        self.skull_cooldown += self.janela.delta_time()
        for i in range(len(self.mobs)):
            face = self.info_mobs[i][3]
            if self.janela.width/2 - 500 < self.mobs[i][face].x < self.janela.width/2 + 500 \
                    and self.janela.height/2 - 500 < self.mobs[i][face].y < self.janela.height/2 + 500 \
                    and not self.info_mobs[i][2] <= 0 and self.info_mobs[i][4] == var.MAPA_FLOOR:

                if ('esqueleto' in self.info_mobs[i][6] or 'necro' in self.info_mobs[i][6])\
                        and self.mobs[i][face].collided(self.player)\
                        and player_hp > 0 and self.cooldown >= 1:
                    var.NECRO_MELEE += 1
                    if var.NECRO_MELEE >= 5:
                        player_hp -= 1
                        var.NECRO_MELEE = 0
                    self.cooldown = 0

                elif self.mobs[i][face].collided(self.player) and player_hp > 0 and self.cooldown >= 1:
                    player_hp -= 1
                    var.PLAYER_HIT = True
                    self.cooldown = 0
                    self.hud.hp = player_hp
                elif self.mobs[i][face].collided(self.player):
                    if self.mobs[i] not in array and len(array) < 8:
                        array.append(self.mobs[i])
                    var.PLAYER_VEL = var.PLAYER_VEL_ORIG - (50 * len(array))
                if 'necromancer' in self.info_mobs[i][6] and self.skull_cooldown >= 5:
                    self.cria_skull(i)
        player_hp = self.skull_seek(player_hp)
        return player_hp

    def cria_skull(self, i):
        if var.NECRODIST <= 350:
            self.necro_skull = Sprite('assets/mobs/death_missile.png', frames=4)
            self.necro_skull.set_total_duration(200)
            self.necro_skull.x = self.mobs[i][self.info_mobs[i][3]].x
            self.necro_skull.y = self.mobs[i][self.info_mobs[i][3]].y
            self.skull_array.append(self.necro_skull)
            self.skull_cooldown = 0

    def skull_seek(self, player_hp):
        for i in self.skull_array:
            if i.x + i.width/2 < self.player.x:
                i.x += 600 * self.janela.delta_time()
                i.set_curr_frame(2)

            elif i.x + i.width/2 > self.player.x + self.player.width:
                i.x -= 600 * self.janela.delta_time()
                i.set_curr_frame(3)

            if i.y + i.height/2 < self.player.y:
                i.y += 600 * self.janela.delta_time()
                i.set_curr_frame(0)

            elif i.y + i.height/2 > self.player.y + self.player.height:
                i.y -= 600 * self.janela.delta_time()
                i.set_curr_frame(1)
            i.draw()
            if i.collided(self.player):
                player_hp -= 1
                self.skull_array.remove(i)
        return player_hp

    def mata_mobs(self):
        for i in range(len(self.mobs)):
            if self.info_mobs[i][2] <= 0:
                self.info_mobs[i][3] = 4
                if 'necro' in self.info_mobs[i][6]:
                    var.NECRO_MORTO = True

    def desenha_inimigos(self):
        for i in range(len(self.mobs)):
            face = self.info_mobs[i][3]
            if self.info_mobs[i][4] == var.MAPA_FLOOR:
                self.mobs[i][face].draw()
                if not self.info_mobs[i][2] <= 0 and self.info_mobs[i][4] == var.MAPA_FLOOR:  # hp e floor
                    if 'esqueleto' in self.info_mobs[i][6]:
                        self.janela.draw_text("{}".format('*' if self.info_mobs[i][2] >= 1 else "-"),
                                              self.mobs[i][face].x + self.mobs[i][face].width/2 - 2,
                                              self.mobs[i][face].y - 10,
                                              20,
                                              (255, 255, 255))

                    elif 'necromancer' in self.info_mobs[i][6]:
                        self.janela.draw_text("{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}".
                                              format('*' if self.info_mobs[i][2] >= 15 else "-",
                                              '*' if self.info_mobs[i][2] >= 14 else "-",
                                              '*' if self.info_mobs[i][2] >= 13 else "-",
                                              '*' if self.info_mobs[i][2] >= 12 else "-",
                                              '*' if self.info_mobs[i][2] >= 11 else "-",
                                              '*' if self.info_mobs[i][2] >= 10 else "-",
                                              '*' if self.info_mobs[i][2] >= 9 else "-",
                                              '*' if self.info_mobs[i][2] >= 8 else "-",
                                              '*' if self.info_mobs[i][2] >= 7 else "-",
                                              '*' if self.info_mobs[i][2] >= 6 else "-",
                                              '*' if self.info_mobs[i][2] >= 5 else "-",
                                              '*' if self.info_mobs[i][2] >= 4 else "-",
                                              '*' if self.info_mobs[i][2] >= 3 else "-",
                                              '*' if self.info_mobs[i][2] >= 2 else "-",
                                              '*' if self.info_mobs[i][2] >= 1 else "-"),
                                              self.mobs[i][face].x - 30,
                                              self.mobs[i][face].y - 10,
                                              20,
                                              (255, 255, 255))
                    else:
                        self.janela.draw_text("{}{}{}{}{}".format('*' if self.info_mobs[i][2] >= 5 else "-",
                                                          '*' if self.info_mobs[i][2] >= 4 else "-",
                                                          '*' if self.info_mobs[i][2] >= 3 else "-",
                                                          '*' if self.info_mobs[i][2] >= 2 else "-",
                                                          '*' if self.info_mobs[i][2] >= 1 else "-"),
                                          self.mobs[i][face].x + 5,
                                          self.mobs[i][face].y - 10,
                                          20,
                                          (255, 255, 255))
