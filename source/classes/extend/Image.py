from source.classes.base.Sprite import BaseSprite
from source.classes.datatypes.UDims import UDim2
from path import Path
import pygame

class Image(BaseSprite):
    def __init__(self, name, imagePath, position = UDim2(), namehint = ''):
        self.filePath = Path(imagePath)
        if not self.filePath.exists():
            raise FileNotFoundError(self.filePath)
        self.img = pygame.image.load(self.filePath, namehint).convert_alpha()
        super().__init__(position, UDim2(00, self.img.get_width(), 0, self.img.get_height()))

    #def render(self, Surface):
    #    Surface.blit(self.img)