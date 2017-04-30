import pygame.transform
from game_instance import Instance
import os
pygame.mixer.pre_init(22050, 16, 2, 1024)

pygame.init()


RESIZABLE = True
screen= pygame.display.set_mode((Assets.WIDTH,Assets.HEIGHT), RESIZABLE)
pygame.display.set_caption('Too Many Weird Aliens')
Assets.load()

virtual_screen = screen.copy()
running = True

game_screen = Instance()

getTicksLastFrame = pygame.time.get_ticks()
while running:

    t = pygame.time.get_ticks()
    # deltaTime in seconds.
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t
    game_screen.update(deltaTime)
    virtual_screen.fill(Assets.BLACK)
    game_screen.draw(virtual_screen)
    x,y = screen.get_size()
    v_ratio = Assets.WIDTH/Assets.HEIGHT
    ratio = x/y
    size = 0,0
    pos = 0,0
    if ratio < v_ratio:
        size = x, x / v_ratio
        pos = 0, (y-size[1])/2
    else:
        size =y * v_ratio, y
        pos = (x - size[0]) / 2,0

    size = int(size[0]),int(size[1])
    temp_screen = pygame.transform.scale(virtual_screen,size)

    screen.fill(Assets.BLACK)
    screen.blit(temp_screen,pos)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            surface = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
        game_screen.pass_event(event)

pygame.quit()

