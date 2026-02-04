import pygame, psutil, math
from source import variables as v

surface = pygame.Surface((800, 600), pygame.SRCALPHA, 32)

def update(process, font, elapsed, dt, fpsDisp):
    fps = v.clock.get_fps()
    memory = process.memory_info().rss / (1024 * 1024)
    if math.floor(elapsed-dt) < math.floor(elapsed):
        fpsDisp = round(fps, 2)
    if fpsDisp % 1 == 0:
        fpsDisp = int(fpsDisp)
    if memory % 1 == 0:
        memory = int(memory)
    fpsTxt = font.render('FPS: ' + str(fpsDisp), True, (255, 255, 255))
    memoryTxt = font.render('Memory usage: ' + str(round(memory, 2)) + ' MB', True, (255, 255, 255))
    #screen.blit(fpsTxt, (2, 2))
    #screen.blit(memoryTxt, (2, 2+2+font.get_height()))
    surface.fill((0, 40, 0, 0))
    surface.blit(fpsTxt, (0, 0))
    surface.blit(memoryTxt, (0, font.get_height()+2))
    surface.set_alpha(int(255/2))
    v.screen.blit(surface, (2, 2))
    return fpsDisp