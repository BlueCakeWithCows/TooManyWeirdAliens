from window import Window
from entity.planets import Earth, Sun
from entity.display import Arrow, StarrySky
from entity.ship import SpaceShip
from pygame import mixer
from entity.enemy import Goblin
import pygame
from math import pi
from misc import GREEN

debug = False


class Instance(Window):
    day = 0
    earth = None
    sun = None
    earth_arrow = None
    ship = None

    def __init__(self):
        Window.__init__(self)

        mixer.music.play(-1)

        self.earth = Earth(self)
        self.sun = Sun(self)
        self.earth_arrow = Arrow(self, self.earth, GREEN, 1)
        self.ship = SpaceShip(self)
        self.camera.target = self.ship
        self.create(StarrySky(self))
        self.create(self.earth)
        self.create(self.sun)
        self.create(self.earth_arrow)
        self.create(self.ship)
        # self.create(VelocityDisplay)
        # self.create(CoordsDisplay)

        # self.update_list.append(Enemy_Spawner.Spawner())

        self.create(Goblin(self, (1300, 200), self.earth))

    def create(self, x):
        if x is not None:
            self.update_list.append(x)
            self.draw_list.append(x)
        else:
            raise ValueError("Cannot add null object to gamelist")

    def listen(self, deltaTime):
        self.day = self.day + 365 * (Assets.EARTH_ANGLULAR_SPEED / (2 * pi)) * deltaTime

        if ((self.ship.health < 1 or self.earth.health < 1) and self.ship in self.update_list):
            self.update_list.remove(self.ship)
            disp = Loss_Display(self.day)
            self.draw_list.append(disp)
            self.update_list.append(disp)

    def pass_event(self, event):
        if (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_k:
                global debug
                debug = not debug
                print("Debug Toggle to ", debug)
