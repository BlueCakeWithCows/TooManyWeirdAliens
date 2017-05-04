from entity.actor import Entity, Drawable
from entity.ship import SpaceShip
from misc import PURPLE
from assets import texture, sound, value
from entity.display import Arrow


class PowerUp(Entity):
    health = 1

    def __init__(self, instance, position, arrow_enable=True):
        Entity.__init__(self, instance)
        self.position = position
        self.radius = value["pickup.size"]
        if arrow_enable:

            self.arrow = Arrow(self, self.instance, PURPLE, 1)
            self.instance.create(self.arrow)

    def inform_collision(self, **kwargs):
        if isinstance(kwargs["obj2"], SpaceShip):
            self.pickup_event(kwargs["obj2"])

    def pickup_event(self, ship):
        pass


class HealthPack(PowerUp):
    def create_drawable(self):
        self.drawable = Drawable(texture["heart"], self.position, False, True)
        self.sound = sound["heal_sound"]

    def pickup_event(self, ship):
        self.sound.player()
        ship.damage(value["pickup.heal_pack_amount"])


class EarthHealPack(PowerUp):
    def create_drawable(self):
        self.drawable = Drawable(texture["repair_earth"], self.position, False, True)
        self.sound = sound["earth_heal"]

    def pickup_event(self, ship):
        self.sound.play()
        self.instance.earth.damage(value["pickup.heal_earth_amount"])
