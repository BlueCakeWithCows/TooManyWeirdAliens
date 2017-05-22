import pygame
import os
import ctypes
ctypes.windll.user32.SetProcessDPIAware()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
pygame.init()
from pygame.locals import *
flags = NOFRAME| DOUBLEBUF
#resolution = (value["init.window_width"], value["init.window_height"])
screen = pygame.display.set_mode((0,0), flags)
print(screen)
from assets import load_assets, load_configs, _systems_path, get_path, texture
load_configs()
load_assets(screen)
print("Passed Configs and Assets")
from weapon import create_bullet_templates
create_bullet_templates()


img = pygame.transform.scale(texture["stat_block_background"],(1440,390))
pygame.image.save(img, "test.png")