#configs first
from assets import value, load_configs,load_assets
load_configs()

#setup display
import pygame
import os
import ctypes

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

#load assets for display
load_assets(screen)
import pygame.transform


from game_instance import Instance

from misc import BLACK



from weapon import create_bullet_templates
create_bullet_templates()
virtual_screen = pygame.transform.scale(screen.copy(), (value["init.virtual_width"], value["init.virtual_height"]))
running = True
game_screen = Instance()
v_ratio = value["init.virtual_width"]/value["init.virtual_height"]


def update(dt):
    game_screen.update(dt)

    for event in pygame.event.get():
        global running
        if event.type == pygame.QUIT:
            running = False

        # if event.type == pygame.VIDEORESIZE and not pygame.FULLSCREEN:
        #     global surface
        #     surface = pygame.display.set_mode((event.w, event.h),
        #                                       pygame.RESIZABLE)
        game_screen.pass_event(event)

virtual_screen = virtual_screen.convert(screen)

def draw(dt):
    virtual_screen.fill(BLACK)
    game_screen.draw(virtual_screen)
    x, y = screen.get_size()
    ratio = x / y
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

    # temp_screen = temp_screen.convert()
    # screen.fill(BLACK)
    screen.blit(temp_screen, pos)

    pygame.display.flip()


last_time = pygame.time.get_ticks()
accumulated_time = 0
dtms= 64
dt = dtms/1000

frames=0
frames_skipped= 0
fps_timer = 0
while running:
    #delta milli seconds
    time= pygame.time.get_ticks()
    dms = time - last_time
    accumulated_time += dms
    last_time = time

    fps_timer += dms
    #update every 16 ms
    if accumulated_time >= dtms:
        frames+=1
        accumulated_time -= dtms
        update(dt)

        #skip frame if needed
        if accumulated_time <dtms:
            pass
            draw(dt)
        else:
            frames_skipped+=1


    if fps_timer>1000:
        fps_timer =- 1000
        avg_fps = 31.25 - frames_skipped / frames * 31.25
        frames_skipped = 0
        frames = 0
        print("avg fps = ", avg_fps)

pygame.quit()
