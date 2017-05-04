from entity.actor import Entity
from assets import texture, sound, value
import pygame


class Projectile(Entity):
    health = 1
    damage = 10
    sound = None
    image = None

    def __init__(self, instance, position, velocity, rotation):
        Entity.__init__(self, instance)
        self.position = position
        self.velocity = velocity
        self._rotation = rotation
        self.radius = value["projectile.size"]
        self._current_rotation=None
        self.rotation= rotation

    def update(self, delta_time):
        Entity.update(self, delta_time)
        if self._current_rotation is not self.rotation and self.image is not None:
            self.drawable.image = pygame.transform.rotate(self.image, self.rotation)
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


