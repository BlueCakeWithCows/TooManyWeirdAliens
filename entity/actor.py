from misc import to_polar, to_rectangular, pythag_distance, GREEN, add_rectangular, scale_rectangular, RED
from pygame import draw, Rect
import pygame
from math import pi
from types import MethodType

# Class should be done 4/24/2017
# Jk 4/25/2017
class Entity:
    destroyed=False
    drawable = None
    visible = True
    _position = 0, 0
    _velocity = 0, 0
    _velocity_polar = 0, 0
    radius = None
    health = None
    max_health= 999999
    arrow = None
    instance = None
    auto_handle_image_rotatation = True
    _current_rotation_image = 0
    _image_rotation = 0
    image = None

    @property
    def image_rotation(self):
        return self._image_rotation
    @image_rotation.setter
    def image_rotation(self, value):
        self._image_rotation = value
        if self.auto_handle_image_rotatation:
            if self._current_rotation_image is not self._image_rotation and self.image is not None and Drawable is not None:
                self.drawable.image = pygame.transform.rotate(self.image, -180 / pi * self._image_rotation)
                self._current_rotation_image = self._image_rotation

    def force_update_image_rotation(self):
        self.drawable.image = pygame.transform.rotate(self.image, -180 / pi * self._image_rotation)
        self._current_rotation_image = self._image_rotation


    # Position and velocity are initilizaed to 0,0 in order to be more forgiving in execution order, ie create image
    # then set position vs other way around
    # Class includes position, velocity, collision (via radius), and health code
    # Feel free to ignore

    # Note, class includes position and velocity code that can be ignored freely (and basic collision)
    # Auto calculates velocity polar - Same is not included for position due to infrequent (never?) use
    # Radius is soley used for debug drawing, may be implemented in sub classes for collisions

    def __init__(self, instance = None):
        self.instance = instance
        self.create_drawable()

    def update(self, delta_time):
        if self.position is not None and self.velocity is not None:
            self.position = add_rectangular(self.position,scale_rectangular(self.velocity,delta_time))

    def create_drawable(self):
        pass

    def destroy(self):
        if (self.arrow is not None):
            self.arrow.destroy()
        if self.instance is not None():
            self.instance.remove(self)

    def damage(self, amount):
        self.health = self.health - amount

        if self.max_health < self.max_health:
            self.health = self.max_health
        if self.health < 1:
            self.on_health_below_zero_event()

    def on_health_below_zero_event(self):
        pass

    def draw(self, screen, offset):
        if self.drawable is not None and self.visible:
            self.drawable.draw(screen, offset)

    def debug_draw(self, screen, offset):
        if self.radius is not None and self.radius > 0:
            pos = int(self.x - offset[0]), int(self.y - offset[1])
            draw.circle(screen, GREEN,
                        pos, self.radius, 1)

    def is_colliding(self, *args):

        # if I ever want to do rectangle collisions :/
        if isinstance(args[0], Rect):
            raise ValueError("Wtf, rectangles aren't supported")
            if len(args) == 2:
                pass
            pass

        # assume point, radius
        point = args[0]
        radius = args[1]
        if pythag_distance(self.position, point) < self.radius + radius:
            return True
        return False

    def is_gui(self):
        if self.drawable is None:
            return False
        else:
            return self.drawable.ignore_offset

    def inform_collision(self, *args):
        pass

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, *args):
        if len(args) == 1:
            self._position = args[0]
        elif len(args) == 2:
            self._position = (args[0], args[1])
        else:
            raise ValueError('Wrong typed passed to position setter. Expected tuple or x and y')
        if self.drawable is not None:
            self.drawable.position = self.position

    @property
    def x(self):
        return self._position[0]

    @property
    def y(self):
        return self._position[1]

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, *args):
        if len(args) == 1:
            self._velocity = args[0]
        elif len(args) == 2:
            self._velocity = (args[0], args[1])
        else:
            raise ValueError('Wrong typed passed to velocity setter. Expected tuple or x and y')
        if self.velocity is not None:
            self._velocity_polar = to_polar(self._velocity)

    @property
    def v_x(self):
        return self._velocity[0]

    @property
    def v_y(self):
        return self._velocity[1]

    @property
    def velocity_polar(self):
        return self._velocity_polar

    @property
    def v_angle(self):
        return self.velocity_polar[1]

    @property
    def v_magnitude(self):
        return self._velocity_polar[0]

    @velocity_polar.setter
    def velocity_polar(self, *args):
        if len(args) == 1:
            self._velocity_polar = args[0]
        elif len(args) == 2:
            self._velocity_polar = (args[0], args[1])
        else:
            raise ValueError('Wrong typed passed to velocity polar setter. Expected tuple or x and y')

        self._velocity = to_rectangular(self._velocity_polar)


class Drawable:
    image = None
    _position = 0, 0
    ignore_offset = False
    draw_from_center = True

    def __init__(self, image=None, position=(0, 0), gui=False, draw_from_center=True):
        self.image = image
        self.center = draw_from_center
        self.ignore_offset = gui
        self._position = position

    def draw(self, screen, camera_offset=(0, 0)):
        if self.image is None:
            return
        if self.ignore_offset:
            x = self.position[0]
            y = self.position[1]
        else:
            x = self.position[0] - camera_offset[0]
            y = self.position[1] - camera_offset[1]
        screen.blit(self.image, (x, y))



    def large(self):
        def replace_draw(self, screen, camera_offset=(0, 0)):
            if self.image is None:
                return
            if self.ignore_offset:
                x = self.position[0]
                y = self.position[1]
            else:
                x = self.position[0] - camera_offset[0]
                y = self.position[1] - camera_offset[1]
            camera_offset = camera_offset[0], camera_offset[1]

            rect = self.image.get_rect(topleft=self.position)
            screen_rect = screen.get_rect(topleft=camera_offset)
            overlap = screen_rect.clip(rect)
            overlap.move_ip(-camera_offset[0], -camera_offset[1])
            #0 is to left
            #> is to right
            corner = overlap.topleft
            area = Rect(0,0,0,0)
            area.size = overlap.size
            if corner[0] == 0:
                area.x = -x
            else:
                area.x= 0
            if corner[1] == 0:
                area.y=-y
            else:
                area.y= 0

            screen.blit(self.image, overlap, area)

        self.draw = MethodType(replace_draw, self)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, *args):
        if len(args) == 1:
            self._position = args[0]
        elif len(args) == 2:
            self._position = (args[0], args[1])
        else:
            raise ValueError('Wrong typed passed to position setter. Expected tuple or x and y')
        if self.draw_from_center and self.image is not None:

            self._position = (self.x - self.image.get_width() / 2, self.y - self.image.get_height() / 2)

    @property
    def x(self):
        return self._position[0]

    @property
    def y(self):
        return self._position[1]
