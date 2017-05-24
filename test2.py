import ctypes
import os

import pygame

ctypes.windll.user32.SetProcessDPIAware()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
pygame.init()
from pygame.locals import *
flags = NOFRAME| DOUBLEBUF
#resolution = (value["init.window_width"], value["init.window_height"])
screen = pygame.display.set_mode((0,0), flags)
print(screen)
from assets import load_assets, load_configs, texture
load_configs()
load_assets(screen)
print("Passed Configs and Assets")
from weapon import create_bullet_templates
create_bullet_templates()
from math import pow, pi
from misc import BLACK, WHITE

import math
refvec = [1,0]
origin = [0,0]
def clockwiseangle_and_distance(point):
    # Vector between point and the origin: v = p - o
    vector = [point[0]-origin[0], point[1]-origin[1]]
    # Length of vector: ||v||
    lenvector = math.hypot(vector[0], vector[1])
    # If length is zero there is no angle
    if lenvector == 0:
        return -math.pi, 0
    # Normalize vector: v/||v||
    normalized = [vector[0]/lenvector, vector[1]/lenvector]
    dotprod  = normalized[0]*refvec[0] + normalized[1]*refvec[1]     # x1*x2 + y1*y2
    diffprod = refvec[1]*normalized[0] - refvec[0]*normalized[1]     # x1*y2 - y1*x2
    angle = math.atan2(diffprod, dotprod)
    # Negative angles represent counter-clockwise angles so we need to subtract them
    # from 2*pi (360 degrees)
    if angle < 0:
        return 2*math.pi+angle, lenvector
    # I return first the angle because that's the primary sorting criterium
    # but if two vectors have the same angle then the shorter distance should come first.
    return angle, lenvector

def get_area(p):
    return 0.5 * abs(sum(x0 * y1 - x1 * y0
                         for ((x0, y0), (x1, y1)) in segments(p)))
def segments(p):
    return zip(p, p[1:] + [p[0]])

def chaikins_corner_cutting(polygon):
    new_poly = []
    length = len(polygon)
    for i in range(length):
        point = polygon[i%length]
        point2 = polygon[(i+1)%length]
        q = .75 * point[0] + .25 * point2[0], .75 * point[1] + .25 * point2[1]
        r = .25 * point[0] + .75 * point2[0], .25 * point[1] + .75 * point2[1]
        new_poly.append(q)
        new_poly.append(r)

    return new_poly

def round_list(stuff):
    new = []
    for x in stuff:
        new.append((round(x[0]),round(x[1])))
    return new

def adjust_list(origin, polygon):
    new_list =[]
    for p in polygon:
        x,y = p
        if x < origin[0]:
            x -=1
        if x > origin[0]:
            x +=1
        if y < origin[1]:
            y -=1
        if y > origin[1]:
            y +=1
        pop = x,y
        new_list.append(pop)
    return new_list

def period(distance):
     return 365 * pow(distance / 15000, 1.5)

class MiniRoid():
#Tp = (ap/ae)^3/2 * Te
    def __init__(self, center_of_mass, index, polygon, orbital_period, distance, angle, rotation, rotation_period):
        self.dict = {}
        self.dict["c"] = center_of_mass
        self.dict["i"] = index
        self.dict["p"] = polygon
        self.dict["o"] = orbital_period
        self.dict["d"] = distance
        self.dict["a"] = angle
        self.dict["r"] = rotation
        self.dict["ro"] = rotation_period


width = 32
height= 32
row=50
minD, maxD = 27000, 30000
minRP, maxRP = 3, 30
img = pygame.Surface((width*row, height*row),pygame.SRCALPHA, 32)

import random

asters = []

min = .09 * width*height
rand = random.Random(2)
aster = texture["asteroid_sheet"]
masked_result = aster.copy()
polygons = []
for x in range(row):
    for y in range(row):
        area=0
        while area<min:
            points = []
            o_x, o_y = 0, 0
            for i in range(rand.randint(3, 14)):
                point = rand.randint(0, width) + x * width, rand.randint(0, height) + y * height
                o_x+=point[0]
                o_y+=point[1]
                points.append(point)
            origin = o_x/len(points), o_y/(len(points))
            points.sort(key=clockwiseangle_and_distance)

            curved_points = chaikins_corner_cutting(points)
            #curved_points = chaikins_corner_cutting(curved_points)
            # curved_points = chaikins_corner_cutting(curved_points)
            curved_points = round_list(curved_points)
            area= get_area(curved_points)


        pygame.draw.polygon(img, WHITE, curved_points)
        polygons.append(curved_points)

        origin = o_x / len(curved_points), o_y / (len(curved_points))
        origin = round(origin[0]), round(origin[1])
        distance = rand.randint(minD, maxD)

        rotation = rand.randint(0,360)/ (180) * pi
        rotation_period = rand.randint(minRP, maxRP)
        orbital_period = period(distance)
        angle = rand.randint(0,360)/ (180) * pi
        roid = MiniRoid(origin, (x,y), curved_points,orbital_period, distance, angle, rotation, rotation_period)
        asters.append(roid.dict)

masked_result.blit(img, (0, 0), None, pygame.BLEND_RGBA_MULT)

for poly in polygons:
    pygame.draw.polygon(masked_result, BLACK, poly, 1)


pygame.image.save(masked_result, "data/assets/textures/asteroids.png")

import json

data = {}

data["width"]=width*8
data["height"]=height*8
data["asteroids"]=asters

json_data = json.dumps(data)
print(json_data)

with open('data/systems/asteroid_belt.txt', 'w') as outfile:
    json.dump(data, outfile)