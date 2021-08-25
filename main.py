from PPlay.window import *
from PPlay.gameimage import *
from menu import *
from jogo import *
from mapa import *
from hud import *
from combate import *
from inimigos import *
from player import *


janela = Window(1600, 900)
janela.set_title("Campanhas de Corsala")
fundo = GameImage("assets/fundo_menu_corsala.jpg")

mapa = Mapa(janela)
player = Player(janela)
jogo = Game(janela, mapa, player)
inimigos = Inimigos(janela, jogo, player)
hud = Hud(janela, jogo.player_hp)

menu = Menu(janela, fundo, jogo)

menu.menu_loop()
