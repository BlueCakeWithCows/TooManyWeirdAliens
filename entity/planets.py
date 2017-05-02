import pygame
from math import pi
from math import cos, sin
from entity.actor import Entity, Drawable
from misc import YELLOW
from assets import value, texture


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
        self.position = x, y
        Entity.__init__(self, instance)

    def create_drawable(self):
        surf = pygame.Surface((self.radius * 2, self.radius * 2))
        pygame.draw.circle(surf, YELLOW, (self.radius, self.radius), self.radius)
        self.drawable = Drawable(surf, self.position, False, True)

    def update(self, delta_time):
        pass


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((300, 300), False)
    import assets

    assets.load_configs()
    assets.load_assets()
    sun = Sun(None)
    earth = Earth(None, sun)
    pygame.quit()
