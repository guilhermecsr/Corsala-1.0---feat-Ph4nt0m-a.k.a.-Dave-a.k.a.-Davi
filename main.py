from PPlay.window import *
from PPlay.gameimage import *
from menu import *

janela = Window(1600, 900)
janela.set_title("Campanhas de Corsala")
fundo = GameImage("assets/fundo_menu.png")

menu = Menu(janela, fundo)

menu.menu_loop()
