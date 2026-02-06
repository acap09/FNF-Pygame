import pygame
import random
import source.registry as reg
import source.variables as v
import source.functions.file_funcs as ff
from source.classes.base.Tween import Tween
from source.classes.extend.Sound import Sound
from source.classes.datatypes.Font import Font
from path import Path as cpath
from pathlib import Path
introTexts = ff.parseTxt(v.source_path / 'data' / 'introTxt.json')
print(introTexts)

curFile = Path(__file__).resolve()

#reg.add('States', curFile.stem, curFile)

#font = pygame.font.Font(v.source_path / 'fonts' / 'fnf.ttf', 20)
font = Font('fonts/fnf.ttf', 20)
font.font.align = pygame.FONT_CENTER
surfaces = {}
freaky = [Sound(cpath('audio/music/freakyMenu.ogg').g(), 102), 0]
freaky[0].play(loops = -1)
freaky[0].set_volume(0)
freaky[1] = v.elapsed
freakyTween = Tween('freadein', freaky[0], 'volume', 0.7, 0.6, 'linear')

texts = [None, None]


def updatePre():
    #print(str(getattr(freaky[0], 'beatHit')) + str(getattr(freaky[0], 'stepHit')))
    '''if freaky[0].stepHit:
        print(f'{v.elapsed}: Step!')
    if freaky[0].beatHit:
        print(f'!!!{v.elapsed}: Beat!!!')
        print(v.registry)'''
    match freaky[0].stepsCount:
        case 18:
            surfaces['introTxt'] = font.render(introTexts[random.randint(1, len(introTexts))-1].lower(),
                                font.SCREENCENTER, True)
        case 30:
            font.change_size(1)
            surfaces['introTxt'] = font.render(surfaces['introTxt']['surfaceArgs'][0].upper(),
                                font.SCREENCENTER, True)


def updatePost():
    pass

def render(dim: tuple):
    for idx, txt in surfaces.items():
        v.mainSurface.blit(txt['surface'], txt['position'].absPos(tupleify=True))

def onDestroy():
    #reg.remove('States', curFile.stem)
    pass