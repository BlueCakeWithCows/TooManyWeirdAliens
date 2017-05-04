import copy
from math import pi

import pygame

from assets import value, texture, sound
from entity.actor import Entity, Drawable
from entity.projectile import Projectile
from misc import add_polar, min_polar, add_rectangular


# Need to replace calls to Assets
# Need to replace Projectile with a projectile template - ?
# Need to move check collision code to appropriate place
class SpaceShip(Entity):
    health = 0
    base_image = None
    base_image_fire = None
    radius = value["ship.radius"]
    channel = None
    speed = 0
    direction = 0

    def __init__(self, instance, position=(0, 0), template=None):
        Entity.__init__(self, instance)
        self.create_drawable()
        self.position = position
        self.health = value["ship.health"]
        self.base_image = texture["ship"]
        self.base_image_fire = texture["ship_fire"]
        self.deacceleration = value["ship.deacceleration"]
        self.auto_deacceleration = value["ship.auto_deacceleration"]
        self.angular_speed = value["ship.rotation_speed"]
        self.acceleration = value["ship.acceleration"]
        self.max_speed = value["ship.max_speed"]
        self.fire_sound = sound["player_fire_sound"]
        self.fire_speed = value["ship.fire_speed"]
        self.projectile = Projectile(instance, None, None, None)
        self.projectile.image = texture["bottle_rocket"]
        self.projectile.sound = sound["earth_hit"]
        self.projectile.damage = value["ship.weapon_damage"]
        self.projectile.speed = value["ship.weapon_speed"]
        self.weapon_velocity = value["ship.weapon_velocity"]

    def create_drawable(self):
        self.drawable = Drawable(texture["ship"], (0, 0), False, True)


    def on_health_below_zero_event(self):
        pass

    def update(self, delta_time):
        self.get_key_inputs()
        self.calculate_new_velocity(delta_time)
        self.calculate_new_position(delta_time)
        self.redraw_image()
        self.fire(delta_time)

    def get_key_inputs(self):
        keys = pygame.key.get_pressed()
        # Possibly better represented as a dictionary or seperate class... whatevs
        self.k_fire = keys[pygame.K_SPACE]
        self.k_up = keys[pygame.K_UP] or keys[pygame.K_w]
        self.k_down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        self.k_right = keys[pygame.K_RIGHT]
        self.k_left = keys[pygame.K_LEFT] or keys[pygame.K_a]

    def calculate_new_velocity(self, delta_time):
        delta_v = 0
        current_v, current_v_angle = self.velocity_polar

        if self.k_down:
            velocity = max(current_v - self.deacceleration * delta_time, 0), current_v_angle
        else:
            velocity = max(current_v - self.auto_deacceleration * delta_time, 0), current_v_angle

        if self.k_left:
            self.direction += delta_time * self.angular_speed
        if self.k_right:
            self.direction -= delta_time * self.angular_speed

        if self.k_up:
            delta_v = self.acceleration * delta_time, self.direction

        velocity = add_polar(delta_v, velocity)
        velocity = min_polar(velocity, self.max_speed)

        self.velocity_polar = velocity()

    def calculate_new_position(self, delta_time):
        delta_position = delta_time * self.v_x, delta_time * self.v_y
        self.position = add_rectangular(self.position, delta_position)

    def redraw_image(self):
        if self.k_up:
            image = self.base_image_fire
        else:
            image = self.base_image
        self.drawable.image = pygame.transform.rotate(image, 180 / pi * self.direction)
        self.drawable.image = self.drawable.image.convert_alpha()

    cooldown = 0

    def fire(self, delta_time):
        self.cooldown = self.cooldown - delta_time
        if (self.cooldown < 0 and self.k_fire):
            self.fire_sound.play()
            self.cooldown = self.fire_speed
            p = copy.copy(self.projectile)
            p.velocity_polar = add_polar(self.velocity_polar, (self.weapon_velocity, self.direction))
            p.rotation = self.direction
            self.instance.create(p)
