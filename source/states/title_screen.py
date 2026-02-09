from source.classes.base.Tween import Tween
from source.classes.extend.AnimatedImage import AnimatedImage
from source.classes.datatypes.UDims import UDim2
import source.variables as v
import pygame

blank = pygame.Surface((1,1), pygame.SRCALPHA)
blank.fill((255, 255, 255))
blank.convert_alpha()
blank.set_alpha(255)
twen = Tween('fade', blank, 'alpha', 0, 2.7, 'easeOutCubic')
twen.play()

test = AnimatedImage('title_screen', 'images/gfDanceTitle.png')
test.add_animation('danceL', 'gfDance', indices=[30, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], fps = 24)
test.add_animation('danceR', 'gfDance', indices=[15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29], fps = 24)

test.scaleSize = UDim2(0.75, 0, 0.75, 0)
test.position = UDim2(0.4, 0, 0.1, 0)

bump = AnimatedImage('logoBump', 'images/logoBumpin.png')
bump.add_animation('bump', 'logo bumpin', fps=24)
#print(bump.animData)

bump.scaleSize = UDim2(0.7, 0, 0.7, 0)
bump.position = UDim2(-0.07, 0, -0.05, 0)

def beat_hit(beat):
    test.stop_anim(False)
    bump.play_anim('bump')
    if beat % 2 == 0:
        test.play_anim('danceL')
    else:
        test.play_anim('danceR')

v.registry['Sound'][v.musicName].beat_hit.connect(beat_hit)

def render(dim):

    #blank.fill((255, 255, 255))
    lblank = pygame.transform.scale(blank, v.mainSurfaceSize)
    v.mainSurface.blit(lblank, (0, 0))
    v.mainSurface.blit(test.img, test.position.absPos(tupleify=True))
    v.mainSurface.blit(bump.img, bump.position.absPos(tupleify=True))