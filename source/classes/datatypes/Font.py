import pygame
from path import Path
from source.classes.datatypes.UDims import UDim2
import source.variables as v
import warnings

class Font():
    SCREENCENTER = '##SCREENCENTER##'
    def __init__(self, fontPath=None, size=12):
        self.fontPath = Path(fontPath).path
        self.size = size
        self.font = pygame.font.Font(self.fontPath, self.size)
    #    self.txtSurfaces = {}

    def renew(self):
        self.renewFont()
    #    self.renewSurfaces()

    def renewFont(self):
        newFont = pygame.font.Font(self.fontPath, self.size)
        for attr in ['bold', 'italic', 'underline', 'strikethrough', 'align', 'point_size']:
            setattr(newFont, attr, getattr(self.font, attr))
        #print('----------------------------\n', self.font)
        self.font = newFont
        #print(self.font, '\n------------------')
    #def renewSurfaces(self):
    #    for idx, txt in self.txtSurfaces.items():
    #        args = txt['surfaceArgs']
    #        self.txtSurfaces[idx]['surface'] = self.font.render(args[0], args[1], args[2], args[3], args[4])

    def change_size(self, size):
        self.size = size
        self.renew()

    def change_font(self, fontPath):
        self.fontPath = Path(fontPath).path
        self.renew()

    def render(self, text, position, antialias, color=(255, 255, 255), bgcolor=None, wraplength=0):
    #    if name in self.txtSurfaces:
    #        warnings.warn(f'Surface named "{name}" already exists! Calling will just replace it.')

        lol = {
            'surface': self.font.render(text, antialias, color, bgcolor, wraplength),
            'surfaceArgs': [text, antialias, color, bgcolor, wraplength],
            'position': position
        }
        if position == '##SCREENCENTER##':
            size = self.font.size(text)
            lol['position'] = UDim2(0.5, -int(size[0] / 2), 0.5, -int(size[1] / 2))
    #    self.txtSurfaces[name] = lol
        return lol

    #def unrender(self, name):
    #    if name not in self.txtSurfaces:
    #        raise KeyError(f"{name} does not exist!")
    #    self.txtSurfaces.pop(name)