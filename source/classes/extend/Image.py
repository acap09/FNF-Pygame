from source.classes.base.Sprite import BaseSprite
from source.classes.datatypes.UDims import UDim2
from path import Path
import source.variables as v
import pygame

class Image(BaseSprite):
    def __init__(self, name, imagePath, position = None, namehint = ''):
        self.filePath = Path(imagePath).path
        super().__init__(name, position)
        self.originalImg = pygame.image.load(self.filePath)
        self.img = self.originalImg.copy()
        self.originalDim = self.img.get_size()
        self.originalSize = UDim2(self.originalDim[0]/v.mainSurfaceSize[0], 0, self.originalDim[1]/v.mainSurfaceSize[
            1], 0)
        self.size = self.originalSize

    def resize(self, *args):
        self.size = UDim2(*args)
        self.img = pygame.transform.scale(self.originalImg, self.size.absPos(tupleify=True))


    def windowResize(self, newDim):
        self.img = pygame.transform.scale(self.originalImg, self.size.absPos(tupleify=True))