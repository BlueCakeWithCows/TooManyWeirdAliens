import pygame
pygame.init()
screen = pygame.display.set_mode((300, 300), False)
from assets import load_assets, load_configs
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