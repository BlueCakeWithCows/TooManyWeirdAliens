import random
from math import cos, sin, pi, floor, ceil

import pygame
from pygame import Surface, Rect

from assets import value, font
from entity.actor import Entity, Drawable
from misc import WHITE, BLACK, distance_and_angle, shift, create_matrix, add_rectangular, sub_rectangular


class Display(Entity):
    text = ""
    color = WHITE
    my_font = None

    def __init__(self, instance, position=(0, 0), text="", color=WHITE, new_font=font, get_text_function=None):
        Entity.__init__(self, instance)
        self.my_font = new_font
        self.text = text
        self.color = color
        self.drawable = Drawable(None, None, True, False)
        self.position = position
        self.get_text_function = get_text_function

    def update(self, delta_time):
        self.update_text()
        self.drawable.image = self.my_font.render(self, 1, self.color)

    def update_text(self):
        if self.get_text_function is not None:
            self.text = self.get_text_function


class Arrow(Entity):
    color = None
    target = None
    scale = 1


    camera = None

    def __init__(self, instance, target, color, size):
        Entity.__init__(self, instance)
        self.scale = size
        self.color = color
        self.target = target
        self.camera = instance.camera
        self.base_image = None
        self.create_base()
        self.ARROW_AXIS_LEFT = value["arrow.left_axis"]
        self.ARROW_AXIS_BOTTOM = value["arrow.bottom_axis"]
        self.ARROW_AXIS_RIGHT = value["arrow.right_axis"]
        self.ARROW_AXIS_TOP = value["arrow.top_axis"]
        self.my_font = font["arrow_font"]

    def create_base(self):
        surf = Surface((64, 32), pygame.SRCALPHA, 32)
        pygame.draw.rect(surf, self.color, Rect(0, 8, 44, 16))
        pygame.draw.polygon(surf, self.color, [(44, 0), (64, 16), (44, 32)])
        # noinspection PyArgumentList
        self.base_image = surf.convert_alpha()
        self.drawable = Drawable(self.base_image.copy(), self.position, True, True)

    def update_image(self):
        if self.instance.camera.point_on_screen(self.target.position):
            self.visible = False
            return
        self.visible = True

        distance, angle = distance_and_angle(
            (self.camera.x + value["init.half_width"], self.camera.y + value["init.half_height"]),
            (self.target.x, self.target.y))

        angle = -angle
        co, si = cos(angle), sin(angle)

        x_axis = self.ARROW_AXIS_LEFT
        if co > 0:
            x_axis = self.ARROW_AXIS_RIGHT
        x_dist = abs((x_axis - value["init.half_width"]) * co)

        y_axis = self.ARROW_AXIS_BOTTOM
        if si > 0:
            y_axis = self.ARROW_AXIS_TOP
        y_dist = abs((y_axis - value["init.half_height"]) * si)

        if x_dist > y_dist:
            new_x = x_axis
            new_y = abs(x_axis - value["init.half_width"]) * -1 * si + value["init.half_height"]
        else:
            new_y = y_axis
            new_x = abs(y_axis - value["init.half_height"]) * co + value["init.half_width"]

        if new_x > self.ARROW_AXIS_RIGHT: new_x = self.ARROW_AXIS_RIGHT
        if new_x < self.ARROW_AXIS_LEFT: new_x = self.ARROW_AXIS_LEFT
        if new_y < self.ARROW_AXIS_TOP: new_y = self.ARROW_AXIS_TOP
        if new_y > self.ARROW_AXIS_BOTTOM: new_y = self.ARROW_AXIS_BOTTOM
        self.position = new_x, new_y
        string = str(int(distance))
        label = self.my_font.render(string, 1, BLACK)

        image = self.base_image.copy()

        if co < 0:
            image.blit(pygame.transform.rotate(label, 180), (10, 6))
        else:
            image.blit(label, (10, 6))
        size = (int(64 * self.scale), int(32 * self.scale))

        self.drawable.image = pygame.transform.rotate(pygame.transform.scale(image, size), angle * 180 / pi)

        print(self.position, " ", self.visible," ", self.drawable.image)

    def update(self, delta_time):
        self.update_image()
    def draw(self, screen, offset):
        print ("yo")
        if self.drawable is not None and self.visible == True:
            self.drawable.draw(screen, offset)

class StarrySky(Entity):

    def __init__(self, instance):
        Entity.__init__(self, instance)
        self.rand = random.Random()
        self.last_position = None
        self.width,self.height = value["init.virtual_width"]/self.d + 2, value["init.virtual_height"]/self.d +2
        self.matrix = create_matrix(ceil(self.height), ceil(self.width))

    def hash(self, i):
        return ((i * 977) % (2 ** 7)) - 64

    def hash2(self, i):
        return (i * 492876847) % (2 ** 12)

    d = 80

    def update(self, delta_time):
        return
        m_x,m_y = self.position = self.instance.camera.position
        if self.last_position is None:
            start_x, start_y = floor(m_x / self.d) , floor(m_y / self.d)
            for col in range(len(self.matrix)):
                for row in range(len(self.matrix[col])):
                    x = col + start_x - 1
                    y = row + start_y - 1
                    self.rand.seed(x + y * (x - y) + (x * y))
                    self.matrix[col][row] = self.rand.randint(-32,32), self.rand.randint(-32,32)
            self.last_position = self.position
        delta = sub_rectangular(self.position, self.last_position)
        if abs(delta[0])> 80:
            self.matrix = shift('left', 1, self.matrix)
            self.last_position = self.position
        if abs(delta[0]) < -80:
            self.matrix = shift('right', 1, self.matrix)
            self.last_position = self.position
        if abs(delta[1])> 80:
            self.matrix = shift('up', 1, self.matrix)
            self.last_position = self.position
        if abs(delta[1]) < -80:
            self.matrix = shift('down', 1, self.matrix)
            self.last_position = self.position


    def draw(self, screen, offset):
        camera_x, camera_y = self.instance.camera.position
        start_x, start_y = floor(camera_x / self.d) - 1, floor(camera_y / self.d)

        end_x, end_y = ceil(start_x + self.width) + 2, ceil(start_y + self.height)
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                self.rand.seed(x + y * (x - y) + (x * y))
                x_pos = self.d * x - camera_x + self.rand.randint(-32, 32)
                y_pos = self.d * y - camera_y + self.rand.randint(-32, 32)
                pygame.draw.circle(screen, WHITE, (int(x_pos), int(y_pos)), 2, 0)