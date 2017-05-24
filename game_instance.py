from math import cos

import pygame
from pygame import mixer

import collision
import entity.planets as planets
import weapon
from assets import music, value, _systems_path
from entity.display import StarrySky
from entity.ship import SpaceShip
from my_gui import Box, InfoBlock, WeaponBar, HealthBar, MiniMap, ItemBar
from system_loader import load_system
from window import Window


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
        self.camera.set_target(self.ship)
        self.camera.offset = (-value["init.half_width"], -value["init.half_height"])
        self.create(StarrySky(self))

        self.system = system = load_system(_systems_path + "sol.sys")
        box =Box(system.system, self)
        box.update()
        #self.add_gui(box)
        #None will be replaced with self after fully implemented.
        self.add_gui(InfoBlock(None))
        self.weapon_bar = WeaponBar(self.ship)
        self.add_gui(self.weapon_bar)

        self.weapon_bar.weapon_slot[0] = weapon.BasicKineticWeapon()
        self.weapon_bar.weapon_slot[1] = weapon.TripleBasicKineticWeapon()
        self.weapon_bar.select(0)
        self.weapon_bar.update()

        self.health_bar = HealthBar(self.ship)
        self.health_bar.update()
        self.add_gui(self.health_bar)

        self.minimap = MiniMap(self.ship, self.system)
        self.add_gui(self.minimap)


        self.item_bar = ItemBar(self.ship)
        self.item_bar.update()
        self.add_gui(self.item_bar)

        self.update_gui()

        for p in system.system_dict.values():
            self.create(p)

        belt = planets.AsteroidBelt(system.get_planet("sol"), "data/systems/asteroid_belt.txt")
        self.create(belt)

        self.ship.position = 22000*cos(0),17000

        # self.update_list.append(Enemy_Spawner.Spawner())
        self.create(self.ship)
        #self.create(Goblin(self, (1300, 200), self.earth))

    def create(self, x):
        if hasattr(x, '__iter__'):
            for p in x:
                self.create(p)
        elif x is not None:
            self.add_update_list.append(x)
            x.instance = self
        else:
            raise ValueError("Cannot add null object to gamelist")

    def listen(self, deltaTime):
        self.minimap.update()
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
            if event.key == pygame.K_1:
                self.weapon_bar.select(0)
            if event.key == pygame.K_2:
                self.weapon_bar.select(1)
            if event.key == pygame.K_3:
                self.weapon_bar.select(2)

    def remove(self, o):
        if o in self.update_list: self.update_list.remove(o)