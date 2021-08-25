import combate
from inimigos import *


class Game:
    def __init__(self, janela, mapa, player):
        self.janela = janela
        self.teclado = Keyboard()
        self.player = player

        # carrega o mapa
        self.mapa = mapa  # .Mapa(self.janela, inimigos)

        # gameimages
        self.fundo = GameImage("assets/fundo_preto.png")

        # combate
        self.combate = combate.Combate(janela, self.player.player)

        self.inimigos = inimigos.Inimigos(janela, Game, self.player.player)

        # atributos
        self.player_hp = 10
        self.hud = hud

        self.mapa_grid = self.mapa.carrega_mapa()
        self.inimigos.cria_mobs(self.mapa_grid)

        # framerate
        self.fps = 0
        self.frames = 0
        self.relogio = 0

    def game_loop(self):
        while True:
            if self.teclado.key_pressed("ESC"):
                break

            self.player.move_player()

            self.mapa.move_player(self.player.player, self.player.velocidade)

            self.fundo.draw()

            self.mapa.desenha_layer(0)

            self.mapa.desenha_layer(1)

            self.inimigos.movimenta_mobs(self.mapa_grid)
            self.player_hp = self.inimigos.dano(self.player_hp)

            self.player.player.draw()

            self.inimigos.desenha_inimigos()

            # carrega direcoes do player
            self.combate.atack(self.mapa.virado_cim, self.mapa.virado_bai, self.mapa.virado_esq, self.mapa.virado_dir, False)

            if self.teclado.key_pressed("SPACE"):
                for i in range(4):
                    self.combate.atack(self.mapa.cim, self.mapa.bai, self.mapa.esq, self.mapa.dir, True)
                    self.combate.desenha_ataque()

            self.mapa.desenha_layer(2)

            # desenha H.U.D.
            self.hud.Hud(self.janela, self.player_hp)
            # self.hud.draw_hud()

            # framerate
            if self.relogio >= 1:
                self.relogio = 0
                self.fps = self.frames
                self.frames = 0

            self.janela.draw_text("fps: {}".format(self.fps), 50, 10, 30, (255, 255, 255))
            self.relogio += self.janela.delta_time()
            self.frames += 1

            self.janela.update()
