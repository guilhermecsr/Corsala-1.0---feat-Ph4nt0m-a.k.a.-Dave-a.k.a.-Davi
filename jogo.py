import combate
from PPlay.mouse import *
from inimigos import *


class Game:
    def __init__(self, janela, mapa, player):
        self.janela = janela
        self.teclado = Keyboard()
        self.player = player
        self.mouse = Mouse()

        # carrega o mapa
        self.mapa = mapa

        # gameimages
        self.fundo = GameImage("assets/fundo_preto.png")
        self.pause = GameImage("assets/pause_menu.png")

        # combate
        self.combate = combate.Combate(janela, self.player)

        self.inimigos = inimigos.Inimigos(janela, Game, self.player.player)

        # atributos
        self.player_hp = 10
        self.hud = hud

        self.mapa_grid = self.mapa.aloca_mapa()
        self.mobs = self.inimigos.cria_mobs()
        self.info_mobs = self.inimigos.info_mobs
        self.coordenadas_mobs = self.inimigos.coordenadas_mobs()

        self.cooldown_player = 0

        # framerate
        self.fps = 0
        self.frames = 0
        self.relogio = 0

        # menu de pause
        self.exit = False

        # assets
        # self.button = Sprite("assets/Start_button.png", frames=2)
        # self.button_start = Sprite("assets/Start_button1.png")
        # self.button_exit = Sprite("assets/Exit_button1.png")
        # self.titulo = Sprite("assets/titulo_corsala.png")
        # self.cursor = Sprite("assets/dwarven_gauntlet.png")

        # # assets position
        # self.menu_x = janela.width / 2 - self.button.width / 2
        # self.menu_y = janela.height / 2 - self.button.height / 2
        #
        # self.titulo.x = self.janela.width / 2 - self.titulo.width / 2
        # self.titulo.y = self.janela.height / 2 - self.titulo.height / 2
        #
        # self.button_start.x = self.menu_x
        # self.button_start.y = self.menu_y
        #
        # self.button_exit.x = self.menu_x
        # self.button_exit.y = self.menu_y + self.button.height + 25

    def pause_loop(self):
        while True:
            if self.teclado.key_pressed("ESC"):
                pass
            # cursor
            self.cursor.x, self.cursor.y = self.mouse.get_position()[0], self.mouse.get_position()[1]

            # cliques
            if self.mouse.is_over_object(self.button_exit) and self.mouse.is_button_pressed(1):
                self.exit = True
                break

            self.button_start = Sprite("assets/start_button.png", False, 2)
            self.button_start.set_sequence(0, 1)
            self.button_start.x = (self.janela.width / 2) - (self.button.width / 2)
            self.button_start.y = (self.janela.height / 2) - (self.button.height / 2)

            self.button_exit = Sprite("assets/exit_button.png", False, 2)
            self.button_exit.set_sequence(0, 1)
            self.button_exit.x = self.menu_x
            self.button_exit.y = self.menu_y + self.button.height + 25

            if self.mouse.is_over_object(self.button_start):
                self.button_start.set_curr_frame(1)

            if self.mouse.is_over_object(self.button_start) and self.mouse.is_button_pressed(1):
                break

            if self.mouse.is_over_object(self.button_exit):
                self.button_exit.set_curr_frame(1)

            self.pause.draw()
            self.button_start.draw()
            self.button_exit.draw()
            self.titulo.draw()
            if 550 < self.mouse.get_position()[0] < self.janela.width - 550 - self.cursor.width \
                    and 300 < self.mouse.get_position()[1] < self.janela.height - 200 - self.cursor.height:
                self.cursor.draw()
            self.janela.update()

    def game_loop(self):
        while True:
            if self.teclado.key_pressed("ESC"):
                self.pause_loop()
                if self.exit:
                    self.exit = False
                    break

            self.fundo.draw()

            self.mapa.desenha_layer()

            self.player.move_player()

            self.mapa.move_player(self.player.player, var.PLAYER_VEL)

            # metodos inimigos
            self.inimigos.movimenta_mobs(self.mapa_grid)
            self.player_hp = self.inimigos.dano(self.player_hp)
            self.inimigos.coordenadas_mobs()

            self.inimigos.desenha_inimigos()

            self.player.player.draw()

            # carrega direcoes do player
            self.combate.atack(self.mapa.virado_cim, self.mapa.virado_bai, self.mapa.virado_esq, self.mapa.virado_dir, False)

            # ataque do player
            self.cooldown_player += self.janela.delta_time()
            if self.teclado.key_pressed("a"):
                self.combate.atack(self.mapa.cim, self.mapa.bai, self.mapa.esq, self.mapa.dir, True)
                if self.combate.acerto(self.mobs, self.info_mobs, self.cooldown_player):
                    self.cooldown_player = 0
            self.player.mata_player(self.mobs, self.player_hp)
            self.player.player_toma_dano()

            if var.NECRO_MORTO:
                self.end_loop()

            # desenha H.U.D.
            self.hud.Hud(self.janela, self.player_hp)

            # framerate
            if self.relogio >= 1:
                self.relogio = 0
                self.fps = self.frames
                self.frames = 0

            self.janela.draw_text("fps: {}".format(self.fps), 1000, 10, 30, (255, 255, 255))
            self.relogio += self.janela.delta_time()
            self.frames += 1

            self.janela.update()

    def end_loop(self):
        while True:
            self.fundo.draw()
            self.titulo.draw()

            self.janela.draw_text("Obrigado!".format(self.fps), 380, 450, 200, (255, 255, 255))

            if self.teclado.key_pressed("ESC"):
                exit()

            self.janela.update()
