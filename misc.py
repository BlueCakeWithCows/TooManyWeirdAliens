from math import sqrt, pi, atan, cos, sin


def to_polar(a, b = None):
    if b is None:
        a,b=a[0],a[1]
    return distance_and_angle((0,0),(a,b))


def distance_and_angle(a, b):
    dy = b[1] - a[1]
    dx = b[0] - a[0]
    dist = sqrt(dx**2 + dy**2)
    if dx ==0 and dy >0: angle = pi/2
    elif dx == 0 and dy < 0: angle = -pi/2
    elif dx < 0: angle = atan(dy/dx)+ pi
    elif dx == 0 and dy ==0: angle = 0
    else: angle = atan(dy/dx)
    angle = angle%(2*pi)
    return dist, angle


def pythag_distance(a, b):
    dy = b[1] - a[1]
    dx = b[0] - a[0]
    return sqrt(dx ** 2 + dy ** 2)


def add_rectangular(a, b):
    z = a[0] + b[0], a[1]+b[1]
    return z


def to_rectangular(a,b= None):
    if b is None:
        a,b=a[0],a[1]
    return cos(b)*a, sin(b)*a


def add_polar(a,b):
    rectangular = add_rectangular(to_rectangular(a), to_rectangular(b))
    return to_polar(rectangular)


def min_polar(polar, limit):
    speed = min(polar[0], limit)
    return (speed, polar[1])


def max_polar(polar, limit):
    speed = max(polar[0], limit)
    return (speed, polar[1])




BLUE = 0, 0, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
YELLOW = 255, 255, 0
PURPLE = 153, 0, 153
WHITE = 255, 255, 255