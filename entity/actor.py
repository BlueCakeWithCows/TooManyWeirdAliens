from misc import to_polar, to_rectangular, pythag_distance, GREEN
from pygame import draw, Rect

#Class should be done 4/24/2017
#Jk 4/25/2017
class Entity:

    drawable = None
    visible = True
    _position = 0, 0
    _velocity = 0, 0
    _velocity_polar = 0, 0
    radius = None
    health = None
    arrow = None
    instance = None
    #Position and velocity are initilizaed to 0,0 in order to be more forgiving in execution order, ie create image
    #then set position vs other way around
    #Class includes position, velocity, collision (via radius), and health code
    #Feel free to ignore

    #Note, class includes position and velocity code that can be ignored freely (and basic collision)
    #Auto calculates velocity polar - Same is not included for position due to infrequent (never?) use
    #Radius is soley used for debug drawing, may be implemented in sub classes for collisions

    def __init__(self, instance):
        self.instance = instance
        self.create_drawable()


    def update(self, delta_time):
        pass

    def create_drawable(self):
        pass

    #Add reference to instance
    def destroy(self):
        if(self.arrow is not None):
            self.arrow.destroy()
        pass

    def damage(self, amount):
        self.health = self.health - amount
        if self.health < 1:
            self.on_health_below_zero_event()

    def on_health_below_zero_event(self):
        pass

    def draw(self, screen, offset):
        if self.drawable is not None and self.visible == True:
            self.drawable.draw(screen, offset)

    def debug_draw(self, screen, offset):
        if self.radius is not None and self.radius > 0:
            pos = int(self.x - offset[0]), int(self.y-offset[1])
            draw.circle(screen, GREEN,
                               pos, self.radius,    1)

    def is_colliding(self, *args):

        #if I ever want to do rectangle collisions :/
        if isinstance(args[0], Rect):
            raise ValueError("Wtf, rectangles aren't supported")
            if len(args) == 2:
                pass
            pass

        #assume point, radius
        point = args[0]
        radius = args[1]
        if pythag_distance(self.position, point)[0] < self.radius + radius:
            return True
        return False

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
            self._position = (args[0],args[1])
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
            self.velocity_polar = args[0]
        elif len(args) == 2:
            self.velocity_polar = (args[0], args[1])
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
        self._position = position
        self.center = draw_from_center
        self.ignore_offset = gui

    def draw(self, screen, camera_offset=(0,0)):
        if self.ignore_offset:
            x = self.screen_x
            y = self.screen_y
        else:
            x = self.screen_x - camera_offset[0]
            y = self.screen_y - camera_offset[1]
        screen.blit(self.image, (x,y))

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
        if self.draw_from_center:
            self._position = (self.x-self.image.get_width()/2, self.y - self.image.get_height()/2)

    @property
    def x(self):
        return self._position[0]

    @property
    def y(self):
        return self._position[1]

