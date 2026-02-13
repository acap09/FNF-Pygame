from source.classes.base.Sprite import BaseSprite
from source.classes.datatypes.UDims import UDim2
from path import Path
import source.variables as v
import pygame

class Image(BaseSprite):
    def __init__(self, name: str, imagePath: str, position: UDim2 = None, namehint = ''):
        self.filePath = Path(imagePath).path
        super().__init__(name, position)
        self.originalImg = pygame.image.load(self.filePath)
        self.img = self.originalImg.copy()
        self.originalDim = self.img.get_size()
        self.originalSize = UDim2(self.originalDim[0]/v.mainSurfaceSize[0], 0, self.originalDim[1]/v.mainSurfaceSize[
            1], 0)
        self.size = self.originalSize
        self.surface = v.mainSurface
        self.refrect = None

    def resize(self, surface = None, *args):
        self.size = UDim2(*args)
        self.refrect = surface.get_rect() if isinstance(surface, pygame.Surface) else None
        self.img = pygame.transform.smoothscale(self.originalImg.convert_alpha(), self.size.absPos(self.refrect, True))
    def update_size(self):
        self.img = pygame.transform.smoothscale(self.originalImg.convert_alpha(), self.size.absPos(self.refrect, True))

    def flip(self, flip_x: bool, flip_y: bool) -> None:
        self.img = pygame.transform.flip(self.originalImg, flip_x, flip_y)


    def windowResize(self, newDim):
        if len(self.groups()) <= 0:
            self.update_size()