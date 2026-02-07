from nturl2path import pathname2url

import pygame
import random
import source.variables as v
import source.functions.file_funcs as ff
#import source.functions.invert as invert
from source.classes.base.Tween import Tween
from source.classes.extend.Sound import Sound
from source.classes.datatypes.UDims import UDim2
from source.classes.datatypes.Font import Font
from source.classes.extend.Image import Image
import source.backend.loops.state as state
from path import Path as cpath
from pathlib import Path
from types import MethodType as method
introTexts = ff.parseTxt(v.source_path / 'data' / 'introTxt.json')
for n, txt in enumerate(introTexts.copy()):
    thing = txt.split('\n')
    thing[0] += str('\n')
    introTexts[n] = thing
print(introTexts)

curFile = Path(__file__).resolve()

#reg.add('States', curFile.stem, curFile)

#font = pygame.font.Font(v.source_path / 'fonts' / 'fnf.ttf', 20)
pat = cpath('fonts/phantommuff_full.ttf').path
font = Font('intro', pat, (20/563, 0))
font.align = pygame.FONT_CENTER

#pat2 = cpath('fonts/phantommuff_empty.ttf').path
#font2 = Font('intro2', pat2, (20/563, 0))
#font2.align = pygame.FONT_CENTER

surfaces = {}
filePath = cpath('audio/music/freakyMenu.ogg')
filePathS = str(filePath)
Sound(filePath, 102)
print(v.registry)
v.registry['Sound'][filePathS].play(loops = -1)
v.registry['Sound'][filePathS].set_volume(0)
freakyTween = Tween('freadein', v.registry['Sound'][filePathS], 'volume', 0.7, 0.6, 'linear')

newground = Image('newground', 'images/newgrounds_logo.png')
newground.resize(0, 50, 0, 15)
newground.visible = False

texts = [None, None]

stepDone = []
def updatePre():
    #print(str(getattr(v.registry['Sound'][filePathS], 'beatHit')) + str(getattr(v.registry['Sound'][filePathS], 'stepHit')))
    '''if v.registry['Sound'][filePathS].stepHit:
        print(f'{v.elapsed}: Step!')
    if v.registry['Sound'][filePathS].beatHit:
        print(f'!!!{v.elapsed}: Beat!!!')
        print(v.registry)'''
    pass

def renderFont(text: str, position: UDim2 | str = None,antialias: bool = True, color = (255, 255, 255), name: str =
None, background=None, wrap_length = 0):
    print('treat')
    font.render(text, position, antialias, color, name, background, wrap_length)
    #font2.render(text, position, antialias, color, name, background, wrap_length)
def changeText(name, text):
    font.change_text(name ,text)
    #font2.change_text(name, text)

randomPick = introTexts[random.randint(0, len(introTexts)-1)]
def step_hit(self, step):
    global font
    print(step)
    match step+5:
        case 10:
            print("YYYY")
            renderFont('PIE ENGINE\n ', v.ALIGN_CC, name='introTxt')
        case 16:
            changeText('introTxt', 'PIE ENGINE\nWITH PYGAME-CE')
        case 22:
            changeText('introTxt', 'NOT ASSOCIATED WITH\n \n \n \n ')
        case 33:
            newground.visible = True
            changeText('introTxt', 'NOT ASSOCIATED WITH\nNEWGROUNDS\n \n \n ')
            newground.resize(269/1409, 0, 261/793, 0)
            newground.position = UDim2(0.5, -int(newground.img.get_width()/2), 0.5, 5)
        case 38:
            changeText('introTxt', randomPick[0].upper()+' ')
            newground.visible = False
        case 48:
            changeText('introTxt', (randomPick[0]+randomPick[1]).upper())
        case 52:
            changeText('introTxt', 'FRIDAY\n \n ')
        case 57:
            changeText('introTxt', 'FRIDAY\nNIGHT\n ')
        case 62:
            changeText('introTxt', 'FRIDAY\nNIGHT\nFUNKIN\'')
        case 69:
            font.unrender('introTxt')
            state.changeState('title_screen')

v.registry['Sound'][filePathS].step_hit = method(step_hit, v.registry['Sound'][filePathS])



def updatePost():
    pass

def render(dim: tuple):
    def rend(surface, pos):
        v.mainSurface.blit(surface, pos)
    for idx, txt in font.surfaces.items():
        if txt['visible']:
            rend(txt['surface'], txt['position'].absPos(tupleify=True))
    if newground.visible:
        rend(newground.img, newground.position.absPos(tupleify = True))
    #if v.registry['Sound'][filePathS].stepsCount == 33:
    #    pygame.image.save(v.mainSurface, Path('./test.png'))

def onDestroy(newState):
    #reg.remove('States', curFile.stem)
    pass