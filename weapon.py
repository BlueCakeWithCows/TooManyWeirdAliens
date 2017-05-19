import copy
from entity.actor import Entity, Drawable
from misc import to_polar, add_rectangular, add_polar, to_rectangular
from assets import texture, sound
class Weapon:


    def __init__(self):
        self.properties = {}
        self.timer = 0
        empty_icon = texture["weapon0_icon"]


    @property
    def projectile_template(self):
        return self.properties.get('projectile_template', None)

    @projectile_template.setter
    def projectile_template(self, value):
        self.properties['projectile_template'] = value

    @property
    def cooldown(self):
        return self.properties.get('cooldown', None)

    @cooldown.setter
    def cooldown(self, value):
        self.properties['cooldown'] = value

    @property
    def icon(self):
        return self.properties.get('icon', None)

    @icon.setter
    def icon(self, value):
        self.properties['icon'] = value

    @property
    def automatic(self):
        return self.properties.get('automatic', None)

    @automatic.setter
    def automatic(self, value):
        self.properties['automatic'] = value

    def update(self, delta_time):
        self.timer = self.timer - delta_time

    def fire(self, launcher, target):
        pass


class BasicKineticWeapon(Weapon):

    def __init__(self):
        Weapon.__init__(self)
        self.cooldown = 2
        self.icon = texture["weapon1_icon"]
        self.trigger_sound = sound["player_fire_sound"]
        self.automatic = True
        self.projectile_template = projectile["player_basic"]

    def fire(self, launcher, target):
            if self.timer > 0:
                return
            self.timer = self.cooldown

            self.trigger_sound.play()
            self.launch_projectile(launcher, launcher.direction)

    def launch_projectile(self, launcher, direction):
        p = copy.copy(self.projectile_template)
        p.position = launcher.position
        p.velocity_polar = add_polar(launcher.velocity_polar, (p.speed, direction))
        p.rotation = direction
        p.create()
        launcher.instance.create(p)


class TripleBasicKineticWeapon(BasicKineticWeapon):
    def __init__(self):
        BasicKineticWeapon.__init__(self)
        self.cooldown=.3

    def fire(self, launcher, target):
        if self.timer > 0:
            return
        self.timer = self.cooldown

        self.trigger_sound.play()
        self.launch_projectile(launcher, launcher.direction-.2)
        self.launch_projectile(launcher, launcher.direction)
        self.launch_projectile(launcher, launcher.direction+.2)



class StraightLineProjectile(Entity):

    def __init__(self, dictionary = None):
        Entity.__init__(self)

    def create_drawable(self):
        self.drawable = Drawable()

    def create(self):
        self.drawable = copy.copy(self.drawable)
        self.image_rotation = self.rotation
        #self.force_update_image_rotation()

    test = True
    bullet_duration = 60
    timer = 0
    def update(self, delta_time):
        Entity.update(self, delta_time)
        #self.image_rotation = self.velocity_polar[1]
        self.timer = self.timer + delta_time
        if self.timer > self.bullet_duration:
            self.instance.remove(self)



def create_bullet_templates():
    global projectile
    projectile = {}
    player_basic = StraightLineProjectile()
    player_basic.speed = 300
    player_basic.damage = 13
    player_basic.radius = 4
    player_basic.bullet_duration = 5
    player_basic.image = texture["bottle_rocket"]
    projectile["player_basic"] = player_basic
    print("Projectiles: ", projectile)


if __name__ == '__main__':
    list = ["fixed_position_fire", "projectile_template", "cooldown", "icon", "trigger_sound", "automatic"]
    for item in list:
        print("@property")
        print("def %s(self):" % item)
        print("return self.properties.get('%s', None)" % item)
        print("@%s.setter" % item)
        print("def %s(self, value):" % item)
        print("self.properties['%s'] = value" % item)