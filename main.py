import pygame
import psutil, os #lllllll
import shutil

pygame.init()
from source import variables as v

icon = pygame.image.load(v.source_path/'placeholder_icon.png')
pygame.display.set_icon(icon)

v.screen = pygame.display.set_mode((1000, 1000*(9/16)), pygame.RESIZABLE)
pygame.display.set_caption('Friday Night Funkin\': Pie Engine')
v.mainSurface = pygame.Surface(v.screen.get_size(), pygame.SRCALPHA, 32)
v.mainSurfaceSize = v.mainSurface.get_size()
v.clock = pygame.time.Clock()

from source.backend.loops import fps_render, render, backend_stuff, state


font = pygame.font.Font(None, 20)
process = psutil.Process(os.getpid())

import source.backend.initialize
fpsDisp = 0
v.clock.tick()
while v.running:
    #v.dt = v.clock.tick()/1000
    v.elapsed += v.dt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            v.running = False
        elif event.type == pygame.WINDOWSIZECHANGED:
            dim = v.screen.get_size()
            #print(dim)
            dim = (int(min(dim[0], int(dim[1]*v.aspectRatio))), int(min(dim[1], int(dim[0]*v.invAspectRatio))))

            #v.mainSurface = pygame.Surface(dim, pygame.SRCALPHA, 32)
            #print(v.mainSurface.get_size())
            print('RESIZED')
            v.mainSurface = pygame.transform.scale(v.mainSurface, dim)
            v.mainSurfaceSize = v.mainSurface.get_size()
            if 'WindowResizeDependencies' in v.registry:
                for idx, val in v.registry['WindowResizeDependencies'].items():
                    if hasattr(val, 'windowResize') and callable(val.windowResize):
                        val.windowResize(dim)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                v.screenshot = True

    fpsDisp, daSurface = fps_render.update(process, font, fpsDisp)
    state.updatePre()
    backend_stuff.update()
    state.update()

    #v.screen.fill((0, 0, 0))
    render.screenClear()
    render.render(fps=[daSurface, (2, 2)])

    v.dt = v.clock.tick(0 if v.fpsLimiter == -1 else v.fpsLimiter)/1000

pygame.display.quit()
pygame.quit()

if v.temp_path.exists() and v.temp_path.is_dir():
    shutil.rmtree(v.temp_path)