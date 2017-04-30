from entity.actor import Entity, Drawable
import random
from misc import distance_and_angle, add_rectangular, to_rectangular, to_polar, pythag_distance, RED
from math import pi, sin, cos
import pygame
from assets import value
from entity.display import Arrow


class Enemy(Entity):
    health = 1
    behavior = None
    image = None
    facing_direction = 0
    speed = 0
    hyper_speed = 0

    def __init__(self, instance):
        Entity.__init__(self, instance)
        self.arrow = Arrow(self, instance, RED, 1)
        self.instance.create(self.arrow)

    #Collision code should be handled in another class
    def collision(self):
        if self.check_collision(Game.game_instance.ship.bounding_box,Game.game_instance.ship.direction):
            Game.game_instance.ship.damage(20)
            Assets.crashing_sound.play()
            self.damage(100)

    def on_health_below_zero_event(self):
        self.destroy()

    def update_image(self):
        self.drawable.image = pygame.transform.rotate(self.image, self.facing_direction * -180/pi)


class Goblin(Enemy):
    
    hyper_speed = value("enemy.goblin_hyper_speed")
    speed = value("enemy.goblin_speed")
    health = value("enemy.goblin_health")
    radius = value("enemy.goblin_radius")
    orbit_distance = value("enemy.goblin_orbit_distance")
    hyper_speed_range = value("enemy.goblin_hyper_speed_range")
    rotation_speed = value("enemy.goblin_rotation_speed")
    weapon_speed = value("enemy.goblin_weapon_speed")
    weapon_damage = value("enemy.goblin_weapon_damage")
    weapon_velocity = value("enemy.goblin_weapon_velocity")

    def __init__(self, instance, position, target):
        Enemy.__init__(self, instance)
        self.target = target
        self.position = position
        self.direction = random.choice([-1,1])
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

        if(distance>self.hyper_speed_range): speed = self.hyper_speed
        else: speed = self.speed
        if distance < self.orbit_distance: self.mode = "DESTROY"

        self.velocity_polar = speed, self.facing_direction
        speed = speed * delta_time
        self.position = add_rectangular(to_rectangular(speed, self.facing_direction))

    timer = 0
    def destroy_mode(self, delta_time):
        self.facing_direction = self.facing_direction + self.direction * self.rotation_speed * delta_time

        new_x, new_y = -cos(self.facing_direction) * self.orbit_distance + self.target.x, -sin(self.facing_direction) * self.orbit_distance + self.target.y
        self.velocity = (new_x - self.x) / delta_time, (new_y - self.y) / delta_time
        self.position = new_x, new_y
        self.fire(delta_time)

        pass

    def fire(self, delta_time):
        self.timer = self.timer - delta_time
        if (self.timer < 0):
            self.timer = self.weapon_speed
            sp, an = to_polar(self.v_x, -self.v_y)
            projectile = Enemy_Projectile(self.position, -(self.angle + pi / 8 * self.direction), sp, an,
                                          self.weapon_damage, RED,
                                          self.weapon_velocity, Assets.goblin_bomb_art)
            self.instance.create(projectile)


        self.update_image()
        self.update_position()
        self.collision()


class Hunter(Enemy):
    hyper_speed = value("enemy.hunter_hyper_speed")
    speed = value("enemy.hunter_speed")
    health = value("enemy.hunter_health")
    radius = value("enemy.hunter_radius")
    weapon_speed = value("enemy.hunter_weapon_speed")
    weapon_damage = value("enemy.hunter_weapon_damage")
    weapon_velocity = value("enemy.hunter_weapon_velocity")
    hyper_speed_range = value("enemy.hunter_hyper_speed_range")

    def __init__(self, instance, position, target):
        Enemy.__init__(self, instance)
        self.target = target
        self.position = position
        self.mode = "SEARCH"

    def create_drawable(self):
        self.drawable = Drawable(Assets.hunter_art, None, False, True)

    timer = 0
    def update(self, delta_time):
        self.timer = self.timer - delta_time
        if self.mode == "SEARCH":
            self.search_mode(delta_time)
        elif self.mode == "DESTROY":
            self.destroy_mode(delta_time)
        self.update_image()

    def search_mode(self, delta_time):
        distance, angle = distance_and_angle(self.position, self.target.position)
        self.facing_direction = angle
        speed = self.speed

        if distance > 1000: speed = self.hyper_speed
        if distance < 200: self.mode = "DESTROY"
        if distance < 400: self.tri_fire()

        self.velocity_polar = speed, angle
        self.position = self.x + self.v_x * delta_time, self.y + self.v_y * delta_time

    def destroy_mode(self, delta_time):
        speed = min(self.speed, self.target.speed)
        self.velocity = speed, self.target.polar_velocity[1]
        self.position = self.x + self.v_x * delta_time, self.y + self.v_y * delta_time
        self.tri_fire()
        if (pythag_distance(self.target.position, self.position) > 800):
            self.mode = "SEARCH"
        pass

    def tri_fire(self):
        if(self.timer < 0):
            self.timer = self.weapon_speed
            distance, direction = distance_and_angle(self.position, self.target.position)
            self.fire(direction + pi / 8)
            self.fire(direction - pi / 8)
            self.fire(direction)


    def fire(self,angle):
        sp, an = self.velocity
        projectile = Enemy_Projectile(self.position,-angle , sp, an,
                                    self.weapon_damage, Assets.RED, self.weapon_velocity, Assets.hunter_rocket_art,.5)
        self.instance.create(projectile)


class Bombarder(Goblin):
    hyper_speed = value("enemy.bombarder_hyper_speed")
    speed = value("enemy.bombarder_speed")
    health = value("enemy.bombarder_health")
    radius = value("enemy.bombarder_radius")
    orbit_distance = value("enemy.bombarder_orbit_distance")
    hyper_speed_range = value("enemy.bombarder_hyper_speed_range")
    rotation_speed = value("enemy.bombarder_rotation_speed")
    weapon_speed = value("enemy.bombarder_weapon_speed")
    weapon_damage = value("enemy.bombarder_weapon_damage")
    weapon_velocity = value("enemy.bombarder_weapon_velocity")
    weapon_duration = value("enemy.weapon_duration")

    def __init(self, instance, position, target):
        Goblin.__init__(self, instance, position, target)
        self.radius = 48

    def create_drawable(self):
        self.drawable = Drawable(Assets.goblin_art, None, False, True)

    timer = 0

    def fire(self, delta_time):
        self.timer = self.timer - delta_time
        if(self.timer<0):
            self.timer = self.weapon_speed
            angle = -pi / 4
            for i in range(10):
                sp, an = self.velocity_polar
                projectile = Enemy_Projectile(self.position, -(self.angle + angle + pi / 8 * self.direction), sp, an,
                                              self.weapon_damage, Assets.RED,
                                              self.weapon_velocity, Assets.bombarder_bomb_art, .5)
                projectile.timer = self.weapon_duration
                self.instance.create(projectile)