from math import sqrt, pi, atan, cos, sin


def to_polar(a, b=None):
    if b is None:
        a, b = a[0], a[1]
    return distance_and_angle((0, 0), (a, b))

def scale_rectangular(a,scale):
    return (a[0]*scale,a[1]*scale)

#http://stackoverflow.com/questions/15023333/simple-tool-library-to-visualize-huge-python-dict
def visualise_dict(d,lvl=0):

    # go through the dictionary alphabetically
    for k in sorted(d):

        # print the table header if we're at the beginning
        if lvl == 0 and k == sorted(d)[0]:
            print('{:<25} {:<15} {:<10}'.format('KEY','LEVEL','TYPE'))
            print('-'*79)

        indent = '  '*lvl # indent the table to visualise hierarchy
        t = str(type(d[k]))

        # print details of each entry
        print("{:<25} {:<15} {:<10}".format(indent+str(k),lvl,t))

        # if the entry is a dictionary
        if type(d[k])==dict:
            # visualise THAT dictionary with +1 indent
            visualise_dict(d[k],lvl+1)

def distance_and_angle(a, b):
    dy = b[1] - a[1]
    dx = b[0] - a[0]
    dist = sqrt(dx ** 2 + dy ** 2)
    if dx == 0 and dy > 0:
        angle = pi / 2
    elif dx == 0 and dy < 0:
        angle = -pi / 2
    elif dx < 0:
        angle = atan(dy / dx) + pi
    elif dx == 0 and dy == 0:
        angle = 0
    else:
        angle = atan(dy / dx)
    angle = angle % (2 * pi)
    return dist, angle


def pythag_distance(a, b):
    dy = b[1] - a[1]
    dx = b[0] - a[0]
    return sqrt(dx ** 2 + dy ** 2)


def add_rectangular(a, b):
    z = a[0] + b[0], a[1] + b[1]
    return z


def sub_rectangular(a, b):
    z = a[0] - b[0], a[1] - b[1]
    return z


def to_rectangular(a, b=None):
    if b is None:
        a, b = a[0], float(a[1])
    return cos(b) * a, sin(b) * a


def add_polar(a, b):
    rectangular = add_rectangular(to_rectangular(a), to_rectangular(b))
    return to_polar(rectangular)


def min_polar(polar, limit):
    speed = min(polar[0], limit)
    return (speed, polar[1])


def max_polar(polar, limit):
    speed = max(polar[0], limit)
    return (speed, polar[1])


UP, DOWN, LEFT, RIGHT = 'up', 'down', 'left', 'right'

def create_matrix(width, height):
    return [[0 for x in range(width)] for y in range(height)]

def shift(direction, number, matrix):
    ''' shift given 2D matrix in-place the given number of rows or columns
        in the specified (UP, DOWN, LEFT, RIGHT) direction and return it
    '''
    if direction in (UP, DOWN):
        n =  (number % len(matrix) if direction == UP else
            -(number % len(matrix)))
        h = matrix[:n]
        del matrix[:n]
        matrix.extend(h)
        return matrix
    elif direction in (LEFT, RIGHT):
        n =  (number % len(matrix[0]) if direction == LEFT else
            -(number % len(matrix[0])))
        temp = list(zip(*matrix))
        h = temp[:n]
        del temp[:n]
        temp.extend(h)
        matrix[:] = map(list, zip(*temp))
        return matrix
    else:
        return matrix

BLUE = 0, 0, 255
BLACK = 0, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
YELLOW = 255, 255, 0
PURPLE = 153, 0, 153
WHITE = 255, 255, 255
