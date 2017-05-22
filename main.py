#configs first
from assets import value, load_configs,load_assets
load_configs()

#setup display
import pygame
import os
import ctypes
from pgu.timer import Speedometer
ctypes.windll.user32.SetProcessDPIAware()

pygame.mixer.pre_init(22050, 16, 16, 512)

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

pygame.init()
pygame.mixer.set_num_channels(32)

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
dtms= 32
dt = dtms/1000

frames=0
frames_skipped= 0
fps_timer = 0
pgu_fps = Speedometer()
pgu2_fps = Speedometer()
while running:
    #delta milli seconds
    time= pygame.time.get_ticks()
    dms = time - last_time
    accumulated_time += dms
    last_time = time

    #update every 16 ms
    if accumulated_time >= dtms:
        frames+=1
        accumulated_time = accumulated_time - dtms
        update(dt)
        pgu2_fps.tick()
        fps_timer += dtms
        #skip frame if needed
        if accumulated_time <dtms:
            pgu_fps.tick()
            draw(dt)
        else:
            frames_skipped+=1


    if fps_timer>5000:
        fps_timer -= 5000
        print("Update fps = ", pgu2_fps.fps)
        print("Graphics fps", pgu_fps.fps)

pygame.quit()
