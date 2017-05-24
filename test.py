import pygame
import os
import ctypes
ctypes.windll.user32.SetProcessDPIAware()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
pygame.init()
from pygame.locals import *
flags = NOFRAME| DOUBLEBUF
#resolution = (value["init.window_width"], value["init.window_height"])
screen = pygame.display.set_mode((0,0), flags)
print(screen)
from assets import load_assets, load_configs, _systems_path, get_path, texture
load_configs()
load_assets(screen)
print("Passed Configs and Assets")
from weapon import create_bullet_templates
create_bullet_templates()

from entity.powerup import EarthHealPack, HealthPack
earth_pack = EarthHealPack(None, (32, 32), False)
heal_pack = HealthPack(None, (-32, -32), False)
print("Passed Powerup")

from entity.planets import Sun
sun = Sun(None)
print("Passed Planets")

from entity.enemy import Goblin, Bombarder, Hunter
g = Goblin(None, (0,0), earth)
b = Bombarder(None, (0,0),earth)
h = Hunter(None, (0,0), earth)
print("Passed Enemies")

from entity.projectile import Projectile
p = Projectile(None, (0,0), (0,0), None)
print("Passed Projectile")

from entity.ship import SpaceShip
ship = SpaceShip(None, (0,0))
print("Passed Player")

from system_loader import load_system

url = get_path(_systems_path + "sol.sys")
system = load_system(url)
print(system.system)

from misc import visualise_dict
visualise_dict(system.system)


from pgu import text, gui as pgui



# pbl = pgui.Label("Alixorian Xanorth II")
# pbl.set_font(font)
# pbl2 = pgui.Label("37342km")
# pbl2.set_font(font2)
# lo.add(pbl,0,20)
# lo.add(pbl2, 150, 22)
# lo.add(button,130,25)
# selector = pgui.Select()
# selector.add("Blue", 'blue')
# selector.add("Green", 'green')
# gun = pgui.Image(texture["repair_earth"])
# selector.add(gun , 'red')
# lo.add(selector, 180, 22)
#

import my_gui

gui = pgui.App()
lo = pgui.Container(width=1920, height=1080)
img = my_gui.InfoBlock()
img.add_to_gui(lo)
import my_gui
p = my_gui.Box(system.system)
p.position = 100,100
p.add_to_gui(lo)
p.update()
container = pgui.Container(width=300, height=100)
container.focusable = False
gah = pgui.Group()

radio_button = pgui.Radio(gah, 'Blue')
radio_button_2 = pgui.Radio(gah, 'Red')
radio_button_3 = pgui.Radio(gah, 'Yellow Mofof')
radio_button.focusable = False
radio_button_2.focusable = False
radio_button_3.focusable = False
container.add(radio_button,100,100)
container.add(radio_button_2,200,100)
container.add(radio_button_3, 300, 100)
container.focus(radio_button_3)
lo.add(container,0,0)

def change_visiblity(value):
    print(value.value)
    print("yolo")


gah.connect(pgui.CHANGE, change_visiblity, gah)

gui.init(lo)




lines = []
lines.append('top line of input')
lines.append('second line of input')
Go = True
while Go:
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            Go=False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            Go = False
        gui.event(event)
    screen.fill((250, 250, 250))
    gui.paint(screen)
    pygame.display.flip()