import pygame
from math import pi
from math import cos, sin
from entity.actor import Entity, Drawable
from misc import YELLOW
from assets import value, texture

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
