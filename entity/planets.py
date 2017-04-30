import pygame
from math import pi
from math import cos,sin
from entity.actor import Entity, Drawable
from misc import YELLOW

class Earth(Entity):

    health = 0

    def __init__(self, instance):
        Entity.__init__(self, instance)
        self.radius = Assets.EARTH_RADIUS
        self.theta = Assets.EARTH_ANGLE
        self.calculate_position()
        self.create_drawable()
        self.health = Assets.EARTH_HEALTH

    def create_drawable(self):
        self.drawable = Basics.Game_Object.Drawable(Assets.earth_art, self.position, False, True)

    def calculate_position(self):
        x = Assets.EARTH_DISANCE * cos(self.theta) + Assets.SUN_X
        y = Assets.EARTH_DISANCE * sin(self.theta) + Assets.SUN_Y
        self.position = (x,y)

    def update(self,delta_time):
        self.theta += Assets.EARTH_ANGLULAR_SPEED * delta_time
        self.theta = self.theta%(2 *pi)
        self.calculate_position()


class Sun(Entity):
    def __init__(self, instance):
        Entity.__init__(self, instance)
        self.radius = Assets.SUN_RADIUS
        x = Assets.SUN_X
        y = Assets.SUN_Y
        self.position = x, y
        self.create_drawable()

    def create_drawable(self):
        surf = pygame.Surface((self.radius * 2, self.radius * 2))
        pygame.draw.circle(surf, YELLOW, (self.radius,self.radius),self.radius)
        surf.convert()
        self.drawable = Drawable(surf, self.x, self.y, False, True)

    def update(self,delta_time):
        pass