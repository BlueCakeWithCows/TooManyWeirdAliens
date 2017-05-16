from window import Window
from entity.planets import Earth, Sun, Planet
from entity.display import Arrow, StarrySky
from entity.ship import SpaceShip
from pygame import mixer
from entity.enemy import Goblin
import pygame
from math import pi
import collision
from misc import GREEN
from assets import music, value, texture, _systems_path
from system_loader import load_system
from my_gui import Box, InfoBlock

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

        self.ship = SpaceShip(self)
        self.camera.target = self.ship
        self.camera.offset = (-value["init.half_width"], -value["init.half_height"])
        self.create(StarrySky(self))

        system = load_system(_systems_path + "sol.sys")
        box =Box(system.system, self)
        box.update()
        self.add_gui(box)
        #None will be replaced with self after fully implemented.
        self.add_gui(InfoBlock(None))
        self.update_gui()

        for p in system.system_dict.values():
            self.create(p)



        # self.update_list.append(Enemy_Spawner.Spawner())
        self.create(self.ship)
        #self.create(Goblin(self, (1300, 200), self.earth))

    def create(self, x):
        if hasattr(x, '__iter__'):
            for p in x:
                self.create(p)
        elif x is not None:
            self.update_list.append(x)
            x.instance = self
        else:
            raise ValueError("Cannot add null object to gamelist")

    def listen(self, deltaTime):
        collision.update(self.collision_list)
        self.day += deltaTime

        # if ((self.ship.health < 1 """or self.earth.health < 1""") and self.ship in self.update_list):
        #     self.update_list.remove(self.ship)
        #     # disp = Loss_Display(self.day)
        #     # self.draw_list.append(disp)
        #     # self.update_list.append(disp)

    def pass_event(self, event):
        Window.pass_event(self, event)
        if (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_k:
                self.debug = not self.debug
                print("Debug Toggle to ", self.debug)
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def remove(self, o):
        if o in self.update_list: self.update_list.remove(o)