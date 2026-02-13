import pygame
import source.variables as v
from source.classes.datatypes.UDims import UDim, UDim2
from source.classes.base.Sprite import BaseSprite

class Internal:
    def __init__(self):
        self.lerp_mult = 1
        self.inv_lerp_mult = 1

class CameraGroup(pygame.sprite.LayeredUpdates):
    LOCKON = '##LOCKON##'
    LERP = '##LERP##'
    def __init__(self, position: UDim2 | tuple = None, size: UDim2 | tuple = None, view_rect: pygame.Rect = pygame.Rect(0, 0, 100, 100)):
        super().__init__()
        if position is None:
            position = UDim2()
        elif isinstance(position, UDim2):
            pass
        elif isinstance(position, tuple):
            position = UDim2(*position)
        else:
            raise TypeError('Position must be UDim2 or tuple!')
        if size is None:
            size = UDim2()
        elif isinstance(size, UDim2):
            pass
        elif isinstance(size, tuple):
            size = UDim2(*size)
        else:
            raise TypeError('Size must be UDim2 or tuple!')

        self.viewport = view_rect
        self.position = position
        self.size = size
        self.disp = pygame.Surface(self.viewport.size, pygame.SRCALPHA)
        self.target: pygame.Surface | BaseSprite | None = None
        self.targetStyle = self.LERP
        self._internal = Internal()

    @property
    def x(self):
        return self.viewport.x
    @property
    def y(self):
        return self.viewport.y


    def draw(self, scale_disp: bool = True) -> list[pygame.Rect|pygame.FRect]:
        self.disp = pygame.Surface(self.viewport.size, pygame.SRCALPHA)
        self.disp.fill((0, 10, 0))
        rects = []
        #print('sprites', self.sprites())
        for sprite in self.sprites():
            rect = sprite.get_rect(self.viewport)
            pos_x = (rect.x - self.x) * sprite.scroll.x
            pos_y = (rect.y - self.y) * sprite.scroll.y
            rects.append(self.disp.blit(sprite.img, (pos_x, pos_y)))
        if scale_disp:
            self.disp = pygame.transform.smoothscale(self.disp, self.size.absPos(tupleify=True))
        return rects

    def align(self, sprite: BaseSprite, _align: str):
        if _align not in v.ALIGNMENTS_2D:
            raise ValueError('Alignment is not of proper syntax!') # what the hell is this wording bro, it sucks
        rect = sprite.get_rect(self.viewport)
        pos = {0:{'sc': 0.0, 'of': 0},1:{'sc': 0.0, 'of': 0}}
        for n, dim in enumerate([_align[2], _align[3]]):
            if dim == 'L':
                pos[n]['sc'] = 0
                pos[n]['of'] = 0
            elif dim == 'C':
                pos[n]['sc'] = 0.5
                pos[n]['of'] = -int(rect.width/2 if n == 0 else rect.height/2)
            elif dim == 'R':
                pos[n]['sc'] = 1
                pos[n]['of'] = -(rect.width if n == 0 else rect.height)
        sprite.position = UDim2(pos[0]['sc'], pos[0]['of'], pos[1]['sc'], pos[1]['of'])



    def update(self, *args, **kwargs):
        if isinstance(self.target, BaseSprite):
            if self.targetStyle == self.LERP:
                self.viewport.centerx += (self.target.get_rect(self.viewport).centerx - self.viewport.centerx) * self.lerp_mult
                self.viewport.centery += (self.target.get_rect(self.viewport).centery - self.viewport.centery) * self.lerp_mult
            elif self.targetStyle == self.LOCKON:
                self.viewport.centerx = self.target.get_rect(self.viewport).centerx
                self.viewport.centery = self.target.get_rect(self.viewport).centery




    @property
    def lerp_mult(self) -> float: #from 0 to 1
        return self._internal.lerp_mult
    @lerp_mult.setter
    def lerp_mult(self, value):
        self._internal.lerp_mult = value
        self._internal.inv_lerp_mult = 1 / value

    @property
    def inv_lerp_mult(self) -> float:
        return self._internal.inv_lerp_mult
    @inv_lerp_mult.setter
    def inv_lerp_mult(self, value): # from 1 to inf, usually more precise
        self._internal.inv_lerp_mult = value
        self._internal.lerp_mult = 1 / value
#print(dir(pygame.sprite.LayeredUpdates))
''' ^^^ Print result for above code ^^^
[
'__bool__', '__class__', '__class_getitem__', '__contains__', 
'__delattr__', '__dict__', '__dir__', '__doc__', 
'__eq__', '__firstlineno__', '__format__', '__ge__', 
'__getattribute__', '__getstate__', '__gt__', '__hash__', 
'__init__', '__init_subclass__', '__iter__', '__le__', 
'__len__', '__lt__', '__module__', '__ne__', 
'__new__', '__reduce__', '__reduce_ex__', '__repr__', 
'__setattr__', '__sizeof__', '__static_attributes__', '__str__', 
'__subclasshook__', '__weakref__', '_init_rect', '_spritegroup', 
'add', 'add_internal', 'change_layer', 'clear', 
'copy', 'draw', 'empty', 'get_bottom_layer', 
'get_layer_of_sprite', 'get_sprite', 'get_sprites_at', 'get_sprites_from_layer', 
'get_top_layer', 'get_top_sprite', 'has', 'has_internal', 
'layers', 'move_to_back', 'move_to_front', 'remove', 
'remove_internal', 'remove_sprites_of_layer', 'sprites', 'switch_layer', 
'update'
]
'''