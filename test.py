import pygame
pygame.init()
screen = pygame.display.set_mode((1920, 1080), False)
from assets import load_assets, load_configs, _systems_path, get_path, texture
load_configs()
load_assets()
print("Passed Configs and Assets")

from entity.powerup import EarthHealPack, HealthPack
earth_pack = EarthHealPack(None, (32, 32), False)
heal_pack = HealthPack(None, (-32, -32), False)
print("Passed Powerup")

from entity.planets import Earth, Sun
sun = Sun(None)
earth = Earth(None, sun)
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

#

gui = pgui.App()
lo = pgui.Container(width=1920)

import planet_box
p = planet_box.Box(system.system)
p.add_to_gui(lo)
p.update()

gui.init(lo)

import planet_box


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