from entity.actor import Entity, Drawable
import random
from misc import distance_and_angle, add_rectangular, to_rectangular, to_polar, add_polar, pythag_distance, RED
from math import pi, sin, cos

import pygame
import copy
from assets import value, texture, sound
from entity.display import Arrow
from entity.projectile import Projectile

class Enemy(Entity):
    health = 1
    behavior = None
    image = None
    facing_direction = 0
    speed = 0
    hyper_speed = 0
    base_projectile =None

    def __init__(self, instance):
        self.base_projectile = Projectile(instance, None, None, None)
        Entity.__init__(self, instance)
        if instance is not None:
            self.arrow = Arrow(instance,self, RED, 1)
            self.instance.create(self.arrow)


    def on_health_below_zero_event(self):
        self.destroy()

    def update_image(self):
        if self.image is not None:
            self.drawable.image = pygame.transform.rotate(self.image, self.facing_direction * -180 / pi)


class Goblin(Enemy):
    hyper_speed = value["enemy.goblin_hyper_speed"]
    speed = value["enemy.goblin_speed"]
    health = value["enemy.goblin_health"]
    radius = value["enemy.goblin_radius"]
    orbit_distance = value["enemy.goblin_orbit_distance"]
    hyper_speed_range = value["enemy.goblin_hyper_speed_range"]
    rotation_speed = value["enemy.goblin_rotation_speed"]
    weapon_speed = value["enemy.goblin_weapon_speed"]
    weapon_damage = value["enemy.goblin_weapon_damage"]
    weapon_velocity = value["enemy.goblin_weapon_velocity"]

    def __init__(self, instance, position, target):
        Enemy.__init__(self, instance)
        self.target = target
        self.position = position
        self.direction = random.choice([-1, 1])
        self.mode = "SEARCH"

    def create_drawable(self):
        self.image = texture["goblin"]
        self.drawable = Drawable(None, None, False, True)
        self.base_projectile.image = texture["goblin_bomb"]
        self.base_projectile.damage = self.weapon_damage
        self.base_projectile.sound = sound["destroyed"]

    def update(self, delta_time):
        if self.mode == "SEARCH":
            self.search_mode(delta_time)
        elif self.mode == "DESTROY":
            self.destroy_mode(delta_time)

        self.update_image()

    def search_mode(self, delta_time):
        distance, angle = distance_and_angle(self.position, self.target.position)
        self.facing_direction = angle

        if (distance > self.hyper_speed_range):
            speed = self.hyper_speed
        else:
            speed = self.speed
        if distance < self.orbit_distance: self.mode = "DESTROY"

        self.velocity_polar = speed, self.facing_direction
        self.position = self.position[0] + self.velocity[0] * delta_time, self.position[1] + self.velocity[1] *delta_time

    timer = 0

    def destroy_mode(self, delta_time):
        self.facing_direction = self.facing_direction + self.direction * self.rotation_speed * delta_time

        new_x, new_y = -cos(self.facing_direction) * self.orbit_distance + self.target.x, -sin(
            self.facing_direction) * self.orbit_distance + self.target.y
        self.velocity = (new_x - self.x) / delta_time, (new_y - self.y) / delta_time
        self.position = new_x, new_y
        self.fire(delta_time)

        pass

    def fire(self, delta_time):
        self.timer = self.timer - delta_time
        if (self.timer < 0):
            self.timer = self.weapon_speed
            p = copy.copy(self.base_projectile)
            p.position = self.position[0], self.position[1]
            p.rotation = self.facing_direction
            p.velocity_polar = add_polar(self.velocity_polar, (self.weapon_velocity,self.facing_direction))
            self.instance.create(p)




class Hunter(Enemy):
    hyper_speed = value["enemy.hunter_hyper_speed"]
    speed = value["enemy.hunter_speed"]
    health = value["enemy.hunter_health"]
    radius = value["enemy.hunter_radius"]
    weapon_speed = value["enemy.hunter_weapon_speed"]
    weapon_damage = value["enemy.hunter_weapon_damage"]
    weapon_velocity = value["enemy.hunter_weapon_velocity"]
    hyper_speed_range = value["enemy.hunter_hyper_speed_range"]

    def __init__(self, instance, position, target):
        Enemy.__init__(self, instance)
        self.target = target
        self.position = position
        self.mode = "SEARCH"

    def create_drawable(self):
        self.drawable = Drawable(texture["hunter"], None, False, True)
        self.base_projectile.drawable = texture["hunter_missile"]
        self.base_projectile.damage = self.weapon_damage
        self.base_projectile.sound = sound["destroyed"]

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
        if (self.timer < 0):
            self.timer = self.weapon_speed
            distance, direction = distance_and_angle(self.position, self.target.position)
            self.fire(direction + pi / 8)
            self.fire(direction - pi / 8)
            self.fire(direction)

    def fire(self, angle):
        p = copy.copy(self.base_projectile)
        p.position = self.position[0], self.position[1]
        p.rotation = self.facing_direction
        p.velocity_polar = self.velocity_polar[0] + self.weapon_velocity, self.velocity_polar[1] + angle
        self.instance.create(p)


class Bombarder(Goblin):
    hyper_speed = value["enemy.bombarder_hyper_speed"]
    speed = value["enemy.bombarder_speed"]
    health = value["enemy.bombarder_health"]
    radius = value["enemy.bombarder_radius"]
    orbit_distance = value["enemy.bombarder_orbit_distance"]
    hyper_speed_range = value["enemy.bombarder_hyper_speed_range"]
    rotation_speed = value["enemy.bombarder_rotation_speed"]
    weapon_speed = value["enemy.bombarder_weapon_speed"]
    weapon_damage = value["enemy.bombarder_weapon_damage"]
    weapon_velocity = value["enemy.bombarder_weapon_velocity"]
    weapon_duration = value["enemy.weapon_duration"]

    def __init(self, instance, position, target):
        Goblin.__init__(self, instance, position, target)
        self.radius = 48

    def create_drawable(self):
        self.drawable = Drawable(texture["bombarder"], None, False, True)
        self.base_projectile.drawable = texture["goblin_bomb"]
        self.base_projectile.damage = self.weapon_damage
        self.base_projectile.sound = sound["destroyed"]

    timer = 0

    def fire(self, delta_time):
        self.timer = self.timer - delta_time
        if (self.timer < 0):
            self.timer = self.weapon_speed
            angle = -pi / 5
            for i in range(10):
                p = copy.copy(self.base_projectile)
                p.position = self.position[0], self.position[1]
                p.rotation = self.facing_direction
                p.velocity_polar = self.velocity_polar[0] + self.weapon_velocity, self.velocity_polar[1] + angle
                self.instance.create(p)
                angle = angle + pi/22.5
