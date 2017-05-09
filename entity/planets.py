import pygame
from math import pi
from math import cos, sin
from entity.actor import Entity, Drawable
from misc import YELLOW
from assets import value, texture

class Planet(Entity):
    def __init__(self, instance, target, radius, image, angle, angular_speed, orbit_radius):
        self.image = image
        self.target = target
        Entity.__init__(self, instance)
        self.radius = radius
        self.theta = angle
        self.distance = orbit_radius
        self.angular_speed = angular_speed

        self.calculate_position()

    def create_drawable(self):
        self.drawable = Drawable(self.image, self.position, False, True)

    def calculate_position(self):
        x = self.distance * cos(self.theta) + self.target.x
        y = self.distance * sin(self.theta) + self.target.y
        self.position = (x, y)

    def update(self, delta_time):
        self.theta += self.angular_speed * delta_time
        self.theta = self.theta % (2 * pi)
        self.calculate_position()


class Earth(Entity):
    health = 0

    def __init__(self, instance, target):
        self.target = target
        Entity.__init__(self, instance)
        self.radius = value["planet.earth_radius"]
        self.theta = value["planet.earth_angle"]
        self.health = value["planet.earth_health"]
        self.distance = value["planet.earth_distance"]
        self.angular_speed = value["planet.earth_angular_speed"]
        self.calculate_position()

    def create_drawable(self):
        self.drawable = Drawable(texture["earth"], self.position, False, True)

    def calculate_position(self):
        x = self.distance * cos(self.theta) + self.target.x
        y = self.distance * sin(self.theta) + self.target.y
        self.position = (x, y)

    def update(self, delta_time):
        self.theta += self.angular_speed * delta_time
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
