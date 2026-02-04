import pygame
from path import Path
import psutil, os
import math
import variables
from source.functions.importfile import importModule

pygame.init()
running = True

screen = pygame.display.set_mode((1000, 1000*(9/16)), pygame.RESIZABLE)
pygame.display.set_caption('Friday Night Funkin\'')
clock = pygame.time.Clock()

font = pygame.font.Font(None, 24)
process = psutil.Process(os.getpid())

dt = 0
elapsed = 0
fpsDisp = 0
while running:
    dt = clock.tick()/1000
    elapsed += dt
    fps = clock.get_fps()
    memory = process.memory_info().rss / (1024*1024)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    if math.floor(elapsed-dt) < math.floor(elapsed):
        fpsDisp = round(fps, 2)
    if fpsDisp % 1 == 0:
        fpsDisp = int(fpsDisp)
    if memory % 1 == 0:
        memory = int(memory)
    fpsTxt = font.render('FPS: ' + str(fpsDisp), True, (255, 255, 255))
    memoryTxt = font.render('Memory usage: ' + str(round(memory, 2)) + ' MB', True, (255, 255, 255))
    screen.blit(fpsTxt, (10, 10))
    screen.blit(memoryTxt, (10, 10+24))
    pygame.display.update()

pygame.display.quit()
pygame.quit()