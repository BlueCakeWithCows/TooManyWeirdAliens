from entity.actor import Entity, Drawable
from entity.ship import SpaceShip
from entity.display import Arrow
from misc import PURPLE


class PowerUp(Entity):
    health = 1
    behavior = None
    image = None
    facing_direction = 0

    def __init__(self, instance, position):
        Entity.__init__(self, instance)
        self.position = position
        self.arrow = Arrow(self, PURPLE, 1)
        self.instance.create(self.arrow)

    def inform_collision(self, **kwargs):
        if isinstance(kwargs["obj2"], SpaceShip):
            self.pickup_event(kwargs["obj2"])


class HealthPack(PowerUp):

    def create_drawable(self):
        self.drawable = Drawable(Assets.heart_art, self.position, False, True)

    def pickup_event(self, ship):
        Assets.heal_sound.play()
        ship.damage(-30)


class EarthHealPack(PowerUp):

    def create_drawable(self):
        self.drawable = Drawable(Assets.repair_earth_art, self.position, False, True)

    def pickup_event(self, ship):
        Assets.earth_heal_sound.play()
        self.instance.earth.damage(-100)