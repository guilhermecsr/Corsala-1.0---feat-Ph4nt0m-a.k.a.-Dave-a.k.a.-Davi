from PPlay.sprite import *


class Hud:
    def __init__(self, janela, hp=1, slots=3):
        self.janela = janela

        self.life = Sprite("assets/hud_life_test.png")
        self.slot = Sprite("assets/hud_frame_test.png")

        self.health_array = []
        self.hud_array = []
        self.hp = hp
        self.itens = slots

        self.pos_inicial_x = 50
        self.pos_inicial_y = janela.height - self.slot.height - 50

        self.health_hud()
        self.heads_up_display()

    def heads_up_display(self):
        for i in range(self.itens):
            self.slot = Sprite("assets/hud_frame_test.png")

            # positcoes
            self.slot.set_position(self.pos_inicial_x + i*60, self.pos_inicial_y)

            self.hud_array.append(self.slot)

            for j in self.hud_array:
                j.draw()

    def health_hud(self):
        for i in range(self.hp):
            self.life = Sprite("assets/hud_life_test.png")

            # positcoes
            self.life.set_position(self.pos_inicial_x + i*60, 50)

            self.health_array.append(self.life)

            for j in self.health_array:
                j.draw()
        return self.health_array

    def draw_hud(self):
        for i in self.hud_array:
            i.draw()

        for i in self.health_array:
            i.draw()
