from assets import value, load_configs,load_assets

load_configs()
import pygame.transform
import pygame
import os
import ctypes
from game_instance import Instance

from misc import BLACK

ctypes.windll.user32.SetProcessDPIAware()

pygame.mixer.pre_init(22050, 16, 2, 1024)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

pygame.init()

RESIZABLE = True
from pygame.locals import *
flags = NOFRAME| DOUBLEBUF
#resolution = (value["init.window_width"], value["init.window_height"])
screen = pygame.display.set_mode((0,0), flags)
print(pygame.display.Info())
pygame.display.set_caption('Too Many Weird Aliens')
load_assets()
virtual_screen = pygame.transform.scale(screen.copy(), (value["init.virtual_width"], value["init.virtual_height"]))
running = True

game_screen = Instance()

getTicksLastFrame = pygame.time.get_ticks()

v_ratio = value["init.virtual_width"]/value["init.virtual_height"]
while running:


    # deltaTime in seconds.
    deltaTime = 0
    while deltaTime == 0:
        t = pygame.time.get_ticks()
        deltaTime = (t - getTicksLastFrame) / 1000.0

    getTicksLastFrame = t
    #print (1/deltaTime)
    game_screen.update(deltaTime)
    virtual_screen.fill(BLACK)
    game_screen.draw(virtual_screen)
    x, y = screen.get_size()
    ratio = x / y
    size = 0, 0
    pos = 0, 0
    if ratio < v_ratio:
        size = x, x / v_ratio
        pos = 0, (y - size[1]) / 2
    else:
        size = y * v_ratio, y
        pos = (x - size[0]) / 2, 0

    size = int(size[0]), int(size[1])
    if size != screen.get_size():
        temp_screen = pygame.transform.scale(virtual_screen, size)
    else:
        temp_screen = virtual_screen
    #temp_screen = temp_screen.convert()
    #screen.fill(BLACK)
    screen.blit(temp_screen, pos)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE and not pygame.FULLSCREEN:
            surface = pygame.display.set_mode((event.w, event.h),
                                             pygame.RESIZABLE)
        game_screen.pass_event(event)

pygame.quit()
