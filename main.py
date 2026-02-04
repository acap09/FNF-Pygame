import pygame
import psutil, os
from source import variables as v
from source.backend.loops import fpsrender, render, backendstuff

pygame.init()

v.screen = pygame.display.set_mode((1000, 1000*(9/16)), pygame.RESIZABLE)
pygame.display.set_caption('Friday Night Funkin\'')
v.clock = pygame.time.Clock()

import source.backend.initialize

font = pygame.font.Font(None, 20)
process = psutil.Process(os.getpid())

dt = 0
elapsed = 0
fpsDisp = 0
while v.running:
    dt = v.clock.tick()/1000
    elapsed += dt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            v.running = False
    backendstuff.update(dt)

    v.screen.fill((0, 0, 0))
    fpsDisp = fpsrender.update(process, font, elapsed, dt, fpsDisp)
    render.render()

pygame.display.quit()
pygame.quit()