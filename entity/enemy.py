from entity.actor import Entity, Drawable
import random
from misc import distance_and_angle, add_rectangular, to_rectangular, to_polar, distance, RED
from math import pi
import pygame
from entity.display import Arrow

class Enemy(Entity):
    health = 1
    behavior = None
    image = None
    facing_direction = 0

    def __init__(self, instance):
        Entity.__init__(self, instance)
        self.arrow = Arrow(self, RED, 1)
        self.instance.create(self.arrow)

    #Collision code should be handled in another class
    def collision(self):
        if self.check_collision(Game.game_instance.ship.bounding_box,Game.game_instance.ship.direction):
            Game.game_instance.ship.damage(20)
            Assets.crashing_sound.play()
            self.damage(100)

    def on_health_below_zero_event(self):
        self.destroy

    def update_image(self):
        self.drawable.image = pygame.transform.rotate(self.image, self.facing_direction * -180/pi)


class Goblin(Enemy):
    target = None
    direction = 0

    def __init__(self, instance, position, target):
        Enemy.__init__(self, instance)
        self.target = target
        self.position = position
        self.direction = random.choice([-1,1])
        self.radius = 24
        self.mode = "SEARCH"


    def create_drawable(self):
        self.drawable = Drawable(Assets.goblin_art, None, False, True)

    def update(self, delta_time):
        if(self.mode == "SEARCH"): self.search_mode(delta_time)
        elif (self.mode == "DESTROY"): self.destroy_mode(delta_time)
        self.update_image()

    def search_mode(self, delta_time):
        distance, angle = distance_and_angle(self.position, self.target)
        self.facing_direction = angle

        if(distance>1200): speed = HYPER_SPEED
        else: speed = SPEED

        self.velocity_polar = speed, facing_direction
        speed = speed * delta_time
        self.position = add_rectangular(to_rectangular(speed, facing_direction))

    timer = 0
    def destroy_mode(self, delta_time):
        self.facing_direction = self.facing_direction + self.direction * Assets.ENEMY_GOBLIN_ROTATION_SPEED * delta_time

        new_x, new_y = -cos(self.facing_direction) * 200 + self.target.x, -sin(self.facing_direction) * 200 + self.target.y
        self.velocity = (new_x - self.x) / delta_time, (new_y - self.y) / delta_time
        self.position = new_x, new_y
        self.fire()

        pass

    def fire(self, delta_time):
        self.timer = self.timer - delta_time
        if (self.timer < 0):
            self.timer = Assets.ENEMY_GOBLIN_DROP_SPEED
            sp, an = to_polar(self.v_x, -self.v_y)
            projectile = Enemy_Projectile(self.position, -(self.angle + pi / 8 * self.direction), sp, an,
                                          Assets.ENEMY_GOBLIN_DROP_DAMAGE, Assets.RED,
                                          Assets.ENEMY_GOBLIN_PROJECTILE_SPEED, Assets.goblin_bomb_art)
            self.instance.create(projectile)


        self.update_image()
        self.update_position()
        self.collision()


class Hunter(Enemy):
    target = None
    arrow = None

    def __init__(self, instance, position, target):
        Enemy.__init__(self, instance)
        self.target = target
        self.position = position

        self.health = Assets.ENEMY_HUNTER_HEALTH
        self.radius = 24
        self.mode = "SEARCH"

    def create_drawable(self):
        self.drawable = Drawable(Assets.hunter_art, None, False, True)

    timer = 0
    def update(self, delta_time):
        self.timer = self.timer - delta_time
        if (self.mode == "SEARCH"):
            self.search_mode(delta_time)
        elif (self.mode == "DESTROY"):
            self.destroy_mode(delta_time)
        self.update_image()

    def search_mode(self, delta_time):
        distance, angle = distance_and_angle(self.position, self.target.position)
        self.facing_direction = angle
        speed = Assets.ENEMY_HUNTER_SPEED

        self.velocity_polar = speed, angle
        self.position = self.x + self.v_x * delta_time, self.y + self.v_y * delta_time

        if distance > 1000: speed = Assets.ENEMY_HUNTER_HYPER_SPEED
        if distance < 200: self.mode = "DESTROY"
        if distance < 400: self.tri_fire()

    def destroy_mode(self, delta_time):
        speed = min(Assets.ENEMY_HUNTER_SPEED, self.target.speed)
        self.velocity = speed, self.target.polar_velocity[1]
        self.position = self.x + self.v_x * delta_time, self.y + self.v_y * delta_time
        self.tri_fire()
        if (distance(self.target.position, self.position) > 800):
            mode = "SEARCH"
        pass

    def tri_fire(self):
        if(self.timer < 0):
            self.timer = Assets.ENEMY_HUNTER_WEAPON_SPEED
            distance, direction = distance_and_angle(self.position, self.target.position)
            self.fire(direction + pi / 8)
            self.fire(direction - pi / 8)
            self.fire(direction)


    def fire(self,angle):
        sp, an = self.velocity
        projectile = Enemy_Projectile(self.position,-angle , sp, an,
                                      Assets.ENEMY_HUNTER_DAMAGE, Assets.RED, Assets.ENEMY_HUNTER_PROJECTILE_SPEED, Assets.hunter_rocket_art,.5)
        self.instance.create(projectile)

def Bombarder(Goblin):
    def __init(self, instance, position, target):
        Goblin.__init__(self, instance, position, target)
        self.radius = 48

    def create_drawable(self):
        self.drawable = Drawable(Assets.goblin_art, None, False, True)

    timer = 0

    def fire(self, delta_time):
        self.timer = self.timer - delta_time
        if(self.timer<0):
            angle = -pi / 4
            for i in range(10):
                sp, an = self.velocity_polar
                projectile = Enemy_Projectile(self.position, -(self.angle + angle + pi / 8 * self.direction), sp, an,
                                              Assets.ENEMY_BOMBARDER_WEAPON_DAMAGE, Assets.RED,
                                              Assets.ENEMY_BOMBARDER_PROJECTILE_SPEED, Assets.bombarder_bomb_art, .5)
                projectile.timer = Assets.ENEMY_BOMBARDER_PROJECTILE_DURATION
                instance.create(projectile)