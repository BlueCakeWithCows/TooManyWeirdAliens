from math import cos, sin
from math import pi

import pygame

import misc
from assets import value, texture
from entity.actor import Entity, Drawable
from misc import YELLOW


class Planet(Entity):
    def __init__(self, name, target, radius, image, angle, orbit_period, orbit_radius):
        self.position = (0,0)
        self.name = name
        self.image = image
        self.target = target
        self.radius = radius
        self.theta = angle
        self.distance = orbit_radius
        self.orbit_period = orbit_period
        self.initial_angle = angle
        Entity.__init__(self, None)
        self.calculate_position()

    def create_drawable(self):
        self.drawable = Drawable(self.image, self.position, False, True)
        self.drawable.large()

    def calculate_position(self):
        if self.target is not None:
            x = self.distance * cos(self.theta) + self.target.x
            y = self.distance * sin(self.theta) + self.target.y
            self.position = (x, y)


    def update(self, delta_time):
        if self.orbit_period is not 0:
            self.theta = self.initial_angle + (self.instance.day / self.orbit_period) * 2 * pi
            self.theta = self.theta % (2 * pi)
            self.calculate_position()


class Sun(Entity):
    def __init__(self, instance):
        self.radius = value["planet.sun_radius"]
        x = value["planet.sun_x"]
        y = value["planet.sun_y"]

        Entity.__init__(self, instance)
        self.position = self.position

    def create_drawable(self):
        surf = pygame.Surface((self.radius * 2, self.radius * 2)).convert()
        pygame.draw.circle(surf, YELLOW, (self.radius, self.radius), self.radius)
        self.drawable = Drawable(surf, self.position, False, True)
    def update(self, delta_time):
        pass
        #Entity.update(self, delta_time)

class AsteroidBelt():

    def __init__(self, sun, url):
        import json
        with open(url) as data_file:
            data = json.load(data_file)
        self.width = data["width"]
        self.height = data["height"]
        self.asteroids = []
        tex= texture["asteroids"]

        self.number_of_groups=80
        self.top_roids = []
        self.frames_since_update = []
        self.next_update = 0
        for i in range(self.number_of_groups):
            self.top_roids.append([])
            self.frames_since_update.append(0)

        for d in data["asteroids"]:
            asteroid = Asteroid(d, sun, self.width,self.height, tex)
            index = int((asteroid.angle%(2*pi))/(2*pi) * self.number_of_groups)
            asteroid.index = index
            self.top_roids[index].append(asteroid)

        self.instance = None #Will be assigned by instance
        self.update_dex = []
        self.to_update = set()



    def update(self, dt):
        d, a = misc.distance_and_angle(self.instance.system.get_planet("sol").position, self.instance.ship.position)
        player_index = int((a % (2 * pi))/(2*pi) *  self.number_of_groups)
        player_index2 = player_index+1
        self.to_update.clear()
        self.to_update.add(player_index)
        self.to_update.add(player_index+1)
        self.to_update.add(player_index - 1)
        self.to_update.add(player_index + 2)
        self.to_update.add(self.next_update)
        self.to_update.add(self.next_update+1)
        self.to_update.add(self.next_update + 2)
        self.to_update.add(self.next_update + 3)
        self.next_update = (self.next_update+4)%self.number_of_groups

        for i in range(len(self.frames_since_update)):
            self.frames_since_update[i] = self.frames_since_update[i] + 1

        for roid_index in self.to_update:
            frames_since_update = self.frames_since_update[roid_index]
            for asteroid in self.top_roids[roid_index]:
                asteroid.update(frames_since_update)
                index = int((asteroid.angle % (2 * pi)) / (2 * pi) * self.number_of_groups)
                if asteroid.index != index:
                    self.top_roids[asteroid.index].remove(asteroid)
                    self.top_roids[index].append(asteroid)
                    asteroid.index = index
            self.frames_since_update[roid_index] = 0



    def draw(self, screen, camera_offset = (0,0)):
        #Minor? optimization missing here
        for roid_index in self.to_update:
            for asteroid in self.top_roids[roid_index]:
                if self.instance.camera.on_screen(asteroid):
                    asteroid.draw(screen, camera_offset)

    def debug_draw(self):
        pass

    def is_gui(self):
        return True

class Asteroid(Entity):

    def __init__(self, dict, target, width, height, texture):
        self.polygon = dict["p"]
        self.center = dict["c"]
        self.index = dict["i"]
        self.orbital_period = dict["o"]
        self.orbital_distance = dict["d"]
        self.angle = dict["a"]
        self.delta_angle = value["init.dt"]/1000 * 2 * pi/self.orbital_period
        self.rotation = dict["r"]
        self.rotation_period = dict["ro"]
        self.rotation_delta_angle = ((value["init.dt"]/1000)*360) /self.rotation_period
        self.target = target
        self.radius = 64

        rect = pygame.Rect(self.index[0]*width,self.index[1]*height,width,height)
        self.sub_surface = texture.subsurface(rect)


        x = self.orbital_distance * cos(self.angle) + self.target.x
        y = self.orbital_distance * sin(self.angle) + self.target.y
        self.position = (x, y)

    def update(self, frames):
        self.angle += self.delta_angle * frames
        self.rotation += self.rotation_delta_angle * frames

        x = self.orbital_distance * cos(self.angle) + self.target.x
        y = self.orbital_distance * sin(self.angle) + self.target.y
        self.position = (x, y)

    def draw(self, screen, camera_offset=(0,0)):

        x = self.x - camera_offset[0] - self.sub_surface.get_width()/2
        y = self.y - camera_offset[1] - self.sub_surface.get_height()/2

        screen.blit(self.sub_surface, (x, y))




