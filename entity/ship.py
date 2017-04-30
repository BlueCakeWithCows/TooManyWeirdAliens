from entity.actor import Entity, Drawable
import pygame
from misc import add_polar, min_polar, add_rectangular
from math import pi, cos, sin


# Need to replace calls to Assets
# Need to replace Projectile with a projectile template - ?
# Need to move check collision code to appropriate place
class SpaceShip(Entity):
    health = 0
    base_image = None
    base_image_fire = None
    base_image_slow = None
    radius = 15
    channel = None
    speed = 0
    direction = 0

    def __init__(self, instance, position=(0, 0), template=None):
        Entity.__init__(self, instance)
        self.create_drawable()
        self.position = position

        self.health = Assets.SHIP_HEALTH

    def create_drawable(self):
        self.drawable = Drawable(Assets.ship_art, (0, 0), False, True)

    def damage(self, amount):
        self.health = self.health - amount
        if (self.health < 1):
            Assets.player_exploded_sound.play()
        return

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
            velocity = max(current_v - Assets.PLAYER_DEACCELERATION * delta_time, 0), current_v_angle
        else:
            velocity = max(current_v - Assets.PLAYER_AUTO_DEACCELERATION * delta_time, 0), current_v_angle

        if self.k_left:
            self.direction += delta_time * Assets.PLAYER_ANGULAR_SPEED
        if self.k_right:
            self.direction -= delta_time * Assets.PLAYER_ANGULAR_SPEED

        if self.k_up:
            delta_v = Assets.PLAYER_ACCELERATION * delta_time, self.direction

        velocity = add_polar(delta_v, velocity)
        velocity = min_polar(velocity, Assets.PLAYER_MAX_SPEED)

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

    # Objects will not be responsible for own collisions
    def check_collision(self):
        # if Game.game_instance.earth.check_collision(self.bounding_box,self.direction):
        #     print("Ouch")
        #     self.damage(1000)
        if Game.game_instance.sun.check_collision(self.bounding_box, self.direction):
            print("Ouch")
            self.damage(1000)

    cooldown = 0

    def fire(self, delta_time):
        self.cooldown = self.cooldown - delta_time
        if (self.cooldown < 0 and self.k_fire):
            Assets.player_fire_sound.play()
            self.cooldown = Assets.GUN_COOLDOWN
            projectile = Projectile(self.position, self.direction, self.speed, self.v_angle, Assets.PLAYER_DAMAGE,
                                    Assets.PURPLE, Assets.PLAYER_PROJECTILE_SPEED, Assets.ship_rocket_art)
            self.instance.create(projectile)
