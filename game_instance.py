from window import Window
from entity.planets import Earth, Sun
from entity.display import Arrow, StarrySky
from entity.ship import SpaceShip
from pygame import mixer
from entity.enemy import Goblin
import pygame
from math import pi
import collision
from misc import GREEN
from assets import music, value

class Instance(Window):
    day = 0
    earth = None
    sun = None
    earth_arrow = None
    ship = None

    def __init__(self):
        Window.__init__(self)
        mixer.music.load(music["song1"])
        mixer.music.play(-1)
        self.collision_list = []
        self.sun = Sun(self)

        self.earth = Earth(self, self.sun)
        self.earth_arrow = Arrow(self, self.earth, GREEN, 1)
        self.ship = SpaceShip(self)
        self.camera.target = self.ship
        self.camera.offset = (-value["init.half_width"], -value["init.half_height"])
        self.create(StarrySky(self))
        self.create(self.earth)
        self.create(self.sun)
        self.create(self.earth_arrow)
        self.create(self.ship)
        # self.create(VelocityDisplay)
        # self.create(CoordsDisplay)

        self.collision_list.append( self.earth)
        self.collision_list.append( self.ship)

        # self.update_list.append(Enemy_Spawner.Spawner())

        self.create(Goblin(self, (1300, 200), self.earth))

    def create(self, x):
        if x is not None:
            self.update_list.append(x)
            self.draw_list.append(x)
        else:
            raise ValueError("Cannot add null object to gamelist")

    def listen(self, deltaTime):
        collision.update(self.collision_list)
        self.day = self.day + 365 * (self.earth.angular_speed / (2 * pi)) * deltaTime

        if ((self.ship.health < 1 or self.earth.health < 1) and self.ship in self.update_list):
            self.update_list.remove(self.ship)
            # disp = Loss_Display(self.day)
            # self.draw_list.append(disp)
            # self.update_list.append(disp)

    def pass_event(self, event):
        if (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_k:
                self.debug = not self.debug
                print("Debug Toggle to ", self.debug)
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def remove(self, o):
        if o in self.draw_list: self.draw_list.remove(o)
        if o in self.update_list: self.update_list.remove(o)