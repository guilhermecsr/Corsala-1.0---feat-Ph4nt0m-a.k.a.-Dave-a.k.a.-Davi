from PPlay.sprite import *


class Hud:
    def __init__(self, janela, hp=1, slots=3):
        self.janela = janela

        self.life = Sprite("assets/jogador/hp_bar_in.png")
        self.bar = Sprite("assets/jogador/hp_bar.png")

        self.health_array = []
        self.hud_array = []
        self.hp = hp
        self.itens = slots

        self.pos_inicial_x = 50
        self.pos_inicial_y = janela.height - self.bar.height - 50

        self.health_hud()

    def health_hud(self):
        for i in range(self.hp):
            self.life = Sprite("assets/jogador/hp_bar_in.png")

            # positcoes
            self.bar.set_position(5, 5)
            self.life.set_position(self.pos_inicial_x + i*self.life.width + 15, 50)

            self.health_array.append(self.life)

            for j in self.health_array:
                j.draw()
                self.bar.draw()
        return self.health_array

    def draw_hud(self):
        for i in self.health_array:
            i.draw()
