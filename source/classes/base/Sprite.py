import source.registry as reg
from source.classes.BaseInstance import BaseInstance
from source.classes.datatypes.UDims import UDim2
import pygame

#class Sprite(BaseInstance):
#    def __init__(self, name: str, dataType: str = None, **kwargs):
#        super().__init__(name, dataType)
#        for key, value in kwargs.items():
#            setattr(self, key, value)
#        if dataType is not None:
#            reg.add(dataType, self.name, self)
#
#    def __repr__(self):
#        return f'<Sprite {self.name}>'
#
#    def get(self, value, fallback = None):
#        return getattr(self, value, fallback)
#
#    def set(self, attr, value):
#        return setattr(self, attr, value)

class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, name: str, position: UDim2 = None, size: UDim2 = None):
        super().__init__()

        self.position = position or UDim2()
        self.size = size or UDim2()
        self.visible = True
        reg.add('WindowResizeDependencies', name, self)

    def __repr__(self):
        return f'<BaseSprite {self.name}>'

    def get(self, value, fallback = None):
        return getattr(self, value, fallback)

    def set(self, value):
        return setattr(self, value)

    def windowResize(self, newDim):
        pass
Sprite = BaseSprite