from source.classes.datatypes.UDims import UDim2
from source.classes.datatypes.Vector2 import Vector2
from source.classes.extend.Camera import CameraGroup
from source.classes.extend.Image import Image
import pygame
import source.variables as v

menuCamGame = CameraGroup(UDim2(), UDim2(1, 0, 1, 0), view_rect=pygame.Rect(0, 0, 1000, 563))

bg = Image('background', 'images/menuBG.png')
#col = pygame.Surface(bg.get_rect().size).convert()
#col.fill((255, 217, 71))
#bg.img.blit(col, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
menuCamGame.add(bg)
bg.resize(menuCamGame.viewport, UDim2(0.1, 0, 0.1, 0))
bg.position = UDim2(1, 0, 1, 0)
#menuCamGame.align(bg, v.ALIGN_CC)
menuCamGame.lerp_mult = 0.1
menuCamGame.target = bg
menuCamGame.targetStyle = menuCamGame.LERP

def update():
    mousePos = pygame.mouse.get_pos()
    bg.position = UDim2(0, mousePos[0], 0, mousePos[1])
    menuCamGame.update()

def render(dim):
    surf, rect = menuCamGame.draw()
    v.mainSurface.blit(surf, menuCamGame.position.absPos(tupleify=True))