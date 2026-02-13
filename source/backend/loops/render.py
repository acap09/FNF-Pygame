import pygame
import source.variables as v
from source.classes.datatypes.Fonts import Font, BitmapFont
from source.classes.extend.Sound import Sound
from path import Path
from datetime import datetime

shutter = Sound(Path('audio/sound/shutter.ogg'))

def screen_clear():
    v.screen.fill((0,0,0))

def render(**kwargs):
    v.mainSurface.fill((0,0,0))
    dim = v.mainSurface.get_size()
    for dataType, objects in v.registry.items():
        for name, obj in objects.copy().items():
            if hasattr(obj, 'render') and callable(obj.render) and not isinstance(obj, (Font, BitmapFont)):
                try:
                    obj.render(dim=dim)
                except Exception as e:
                    print(obj)
                    raise Exception(e)
    for key, value in kwargs.items():
        if isinstance(value, list) and isinstance(value[0], pygame.Surface):
            pos = value[1] if isinstance(value[1], tuple) else (0, 0)
            v.screen.blit(value[0], pos)

    if v.screenshot:
        pygame.image.save(v.mainSurface, v.f11_path/f'Screenshot {datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.png')
        shutter.stop()
        shutter.play()
    v.screenshot = False

    #pygame.display.update()

#def fps_render(surf):
    #v.screen.blit(surf, (2, 2))

def update_disp(fps):
    screenDim = v.screen.get_size()
    v.screen.blit(v.mainSurface, (int((screenDim[0] - v.mainSurfaceSize[0]) / 2), int((screenDim[1] - v.mainSurfaceSize[
        1]) / 2)))
    v.screen.blit(fps, (2, 2))
    pygame.display.update()