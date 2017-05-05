from entity.actor import Entity, Drawable
from assets import texture, sound, value
import pygame
import copy
from math import pi

class Projectile(Entity):
    health = 1
    damage = 10
    sound = None
    image = None

    def __init__(self, instance=None, position=(0,0), velocity=(0,0), rotation=0):
        self.position = position
        Entity.__init__(self, instance)

        self.velocity = velocity
        self._rotation = rotation
        self.radius = value["projectile.size"]
        self._current_rotation=None
        self.rotation= rotation
    def create_drawable(self):
        self.drawable = Drawable()
    def create(self):
        self.drawable = copy.copy(self.drawable)
    def update(self, delta_time):
        Entity.update(self, delta_time)
        if self._current_rotation is not self.rotation and self.image is not None:
            print(self.rotation)
            self.drawable.image = pygame.transform.rotate(self.image, -180/ pi * self.rotation)
            self._current_rotation = self.rotation

    # def inform_collision(self, **kwargs):
    #     if isinstance(kwargs["obj2"], SpaceShip):
    #         kwargs["obj2"].damage()
    #         self.destroy()
    #         sound.play()
    #     if isinstance(kwargs["obj2"], Enemy):
    #         kwargs["obj2"].damage()
    #         self.destroy()
    #         sound.play()
    #     if isinstance(kwargs["obj2"], Earth):
    #         kwargs["obj2"].damage()
    #         self.destroy()
    #         sound.play()


