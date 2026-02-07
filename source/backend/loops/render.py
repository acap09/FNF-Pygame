import pygame
import source.variables as v
from source.classes.datatypes.Font import Font
from source.classes.extend.Sound import Sound
from path import Path
from datetime import datetime

shutter = Sound(Path('audio/sound/shutter.ogg'))

def screenClear():
    v.screen.fill((0,0,0))

def render(**kwargs):
    v.mainSurface.fill((0,0,0))
    dim = v.mainSurface.get_size()
    screenDim = v.screen.get_size()
    for dataType, objects in v.registry.items():
        for name, obj in objects.copy().items():
            if hasattr(obj, 'render') and callable(obj.render) and not isinstance(obj, Font):
                obj.render(dim=dim)
    v.screen.blit(v.mainSurface, (int((screenDim[0]-dim[0])/2), int((screenDim[1]-dim[1])/2)))
    for key, value in kwargs.items():
        if isinstance(value, list) and isinstance(value[0], pygame.Surface):
            pos = value[1] if isinstance(value[1], tuple) else (0, 0)
            v.screen.blit(value[0], pos)

    if v.screenshot:
        pygame.image.save(v.mainSurface, v.f11_path/f'Screenshot {datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.png')
        shutter.stop()
        shutter.play()
    v.screenshot = False

    pygame.display.update()