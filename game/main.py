import pygame
from path import Path

pygame.init()
running = True

screen = pygame.display.set_mode((1000, 1000*(9/16)), pygame.RESIZABLE)
pygame.display.set_caption('Friday Night Funkin\'')
clock = pygame.time.Clock()

#font = pygame.font.Font(None, 48)

dt = 0
while running:
    dt = clock.tick()/1000
    fps = clock.get_fps()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    pygame.display.update()
    finalTime = pygame.time.get_ticks()

pygame.display.quit()
pygame.quit()