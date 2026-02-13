import pygame
import pgbitmapfont as bitmap
from path import Path
from source.classes.datatypes.UDims import UDim, UDim2
import source.registry as reg
import source.variables as v
import warnings
import copy

class Font:
    def __init__(self, name = None, fontPath: str = None, size: UDim | tuple = None):
        if isinstance(size, tuple):
            size = UDim(*size)
        elif isinstance(size, UDim):
            pass
        elif size is None:
            size = UDim()
        else:
            raise TypeError(f'Size must be a UDim or tuple!')
        self.fontPath = Path(fontPath).path
        self.size = size
        self.font: pygame.font.Font = None
        self.oldFont = None
        self.surfaces = {}
        self.renew_font()
        reg.add('Font', name or str(self.fontPath), self)
        reg.add('WindowResizeDependencies', name or str(self.fontPath), self)
        #print('hhhhhhhhhhhhhhhh')

    def renew(self):
        self.renew_font()
        self.renew_surface()
    def renew_font(self):
        if self.fontPath.suffix in ['.json', '.png']:
            raise TypeError('Font does not support PNG files! Did you mean to use BitmapFont?')
        attributes = {}
        exist = isinstance(self.font, pygame.font.Font)
        if exist:
            for attr in ['bold', 'italic', 'underline', 'strikethrough', 'align']:
                attributes[attr] = getattr(self.font, attr)
        self.oldFont = self.font
        if self.fontPath.exists():
            self.font = pygame.font.Font(self.fontPath, int(self.size.absPos()))
        else:
            warnings.warn(f'{self.fontPath} does not exist! Default font will be used instead.')
            self.font = pygame.font.Font(None, int(self.size.absPos()))
        if exist:
            for attr, val in attributes.items():
                setattr(self.font, attr, val)
    def renew_surface(self):
        for name, val in self.surfaces.copy().items():
            prop = self.surfaces[name]
            args = prop['args']
            self.surfaces[name] = {
                'surface': self.font.render(args['text'], args['antialias'], args['color'], args['background'], args['wrap_length']),
                'args': args,
                'position': None,
                'visible': prop['visible']
            }
            self.surfaces[name]['position'] = UDim2(args['position'], self.surfaces[name]['surface'])



    def change_size(self, size: UDim | tuple):
        if not isinstance(size, (UDim, tuple)):
            raise TypeError('Size given must be a UDim!')
        if isinstance(size, tuple):
            size = UDim(*size)
        self.size = size
        self.point_size = self.size.absPos()
        self.renew_surface()
    def change_font(self, fontPath):
        self.fontPath = Path(fontPath).path
        self.renew()

    def change_text(self, name: str, text: str):
        name = str(name)
        text = str(text)
        if name not in self.surfaces:
            raise KeyError(f'{name} does not exist!')
        args = self.surfaces[name]['args']
        args['text'] = text
        self.surfaces[name] = {
            'surface': self.font.render(args['text'], args['antialias'], args['color'], args['background'], args['wrap_length']),
            'args': args,
            'position': None,
            'visible': self.surfaces[name]['visible']
        }
        self.surfaces[name]['position'] = UDim2(args['position'], self.surfaces[name]['surface'])
        #print('hhhhiiii')

    def windowResize(self, newDim: tuple):
        self.point_size = self.size.absPos()
        #print(self.point_size)
        self.renew_surface()

    def unrender(self, name: str):
        if name not in self.surfaces:
            warnings.warn(f'{name} does not exist as a text surface!')
            return
        self.surfaces.pop(name)



    def render(self, text: str, position: UDim2 | str = None,antialias: bool = True, color = (255, 255, 255), name: str = None, background=None, wrap_length = 0) -> pygame.Surface:
        nam = name if isinstance(name, str) else text
        if nam in self.surfaces:
            self.surfaces.pop(nam)
            warnings.warn(f'A TextSurface with name {nam} already exists and therefore will be replaced!')
        self.surfaces[nam] = {
            'surface': self.font.render(text, antialias, color, background, wrap_length),
            'args': {
                'text': text,
                'position': position,
                'antialias': antialias,
                'color': color,
                'background': background,
                'wrap_length': wrap_length,
                'name': name
            },
            'position': None,
            'visible': True
        }
        self.surfaces[nam]['position'] = UDim2(position, self.surfaces[nam]['surface'])
        #print('treatarewt')

    def size(self, text):
        return self.font.size(text)

    def metrics(self, text):
        return self.font.metrics(text)

    def set_script(self, value):
        self.font.set_script(value)

    def set_direction(self, value):
       self.font.set_direction(value)

    def get_bold(self) -> bool:
        return self.font.get_bold()

    def get_italic(self) -> bool:
        return self.font.get_italic()

    def get_underline(self) -> bool:
        return self.font.get_underline()

    def get_strikethrough(self) -> bool:
        return self.font.get_strikethrough()

    def get_point_size(self) -> int:
        return self.font.get_point_size()



    @property
    def bold(self) -> bool:
        return self.font.bold
    @bold.setter
    def bold(self, value):
        self.font.bold = value

    @property
    def italic(self) -> bool:
        return self.font.italic
    @italic.setter
    def italic(self, value):
        self.font.italic = value

    @property
    def underline(self) -> bool:
        return self.font.underline
    @underline.setter
    def underline(self, value):
        self.font.underline = value

    @property
    def strikethrough(self) -> bool:
        return self.font.strikethrough
    @strikethrough.setter
    def strikethrough(self, value):
        self.font.strikethrough = value

    @property
    def align(self) -> int:
        return self.font.align
    @align.setter
    def align(self, value):
        self.font.align = value

    @property
    def point_size(self) -> int:
        return self.font.point_size
    @point_size.setter
    def point_size(self, value):
        self.font.point_size = int(value)

    @property
    def outline(self) -> int:
        return self.font.outline
    @outline.setter
    def outline(self, value):
        self.font.outline = value

    @property
    def name(self) -> str:
        return self.font.name

    @property
    def style_name(self) -> str:
        return self.font.style_name

    @property
    def linesize(self) -> int:
        return self.font.get_linesize()
    @linesize.setter
    def linesize(self, value):
        self.font.set_linesize(value)

    @property
    def height(self) -> int:
        return self.font.get_height()

    @property
    def ascent(self) -> int:
        return self.font.get_ascent()

    @property
    def descent(self) -> int:
        return self.font.get_descent()

fonts = (bitmap.BitmapFont, bitmap.BitmapFontFreeDims, bitmap.BitmapFontFixedHeight)
class BitmapFont:
    def __init__(self, name: str, path: Path, size: UDim=None, spacing: tuple[int, int]=(3,3),
                 fgcolor: pygame.Color=None, default_char: str='\u27c1', **kwargs):
        if isinstance(size, tuple):
            size = UDim(*size)
        elif isinstance(size, UDim):
            pass
        elif size is None:
            size = UDim()
        else:
            raise TypeError(f'Size must be a UDim or tuple!')

        self.fontPath = Path(path).path
        self.size = size
        self.font: bitmap.BitmapFontFreeDims | bitmap.BitmapFontFixedHeight | bitmap.BitmapFont = None
        self.oldFont = None
        self.surfaces = {}
        self.args = {'name': name, 'path': path, 'size': size, 'spacing': spacing, 'fgcolor': fgcolor,
                     'default_char': default_char, 'kwargs': kwargs}
        self.renew_font()
        reg.add('BitmapFont', name or str(self.fontPath), self)
        reg.add('WindowResizeDependencies', name or str(self.fontPath), self)

    def renew(self):
        self.renew_font()
        self.renew_surfaces()
    def renew_font(self):
        if not self.fontPath.suffix in ['.json', '.png']:
            raise TypeError('Font does not support PNG files! Did you mean to use BitmapFont?')

        exists = isinstance(self.oldFont, fonts)
        #attributes = {}
        #if exists:
        self.oldFont = self.font
        self.font = bitmap.BitmapFont(self.fontPath, self.size.absPos(), self.args['spacing'], self.args['fgcolor'],
                                      self.args['default_char'])
    def renew_surfaces(self):
        for name, val in self.surfaces.copy().items():
            prop = self.surfaces[name]
            args = prop['args']
            surface, rect = self.font.render(args['text'], args['fgcolor'], args['align'])
            self.surfaces[name] = {
                'surface': surface,
                'rect': rect,
                'args': args,
                'position': None,
                'visible': prop['visible']
            }
            self.surfaces[name]['position'] = UDim2(args['position'], self.surfaces[name]['surface'])

    def windowResize(self, dim):
        self.renew()



    def unrender(self, name: str):
        if name not in self.surfaces:
            warnings.warn(f'{name} does not exist as a text surface!')
            return
        self.surfaces.pop(name)

    def render(self, text: str, position: UDim2 | str, fgcolor: pygame.Color=None, align: str='LEFT', name: str = None):
        name = text if name is None else str(name)
        if name in self.surfaces:
            self.surfaces.pop(name)
            warnings.warn(f'A TextSurface with name {name} already exists and therefore will be replaced!')
        surface, rect = self.font.render(text, fgcolor, align)
        self.surfaces[name] = {
            'surface': surface,
            'rect': rect,
            'args': {
                'text': text,
                'position': position,
                'fgcolor': fgcolor,
                'align': align,
                'name': name
            },
            'position': None,
            'visible': True
        }
        self.surfaces[name]['position'] = UDim2(position, self.surfaces[name]['surface'])

    def change_text(self, name: str, text: str):
        name = str(name)
        text = str(text)
        if name not in self.surfaces:
            raise KeyError(f'{name} does not exist!')
        args = self.surfaces[name]['args']
        args['text'] = text
        surface, rect = self.font.render(text, args['fgcolor'], args['align'])
        self.surfaces[name] = {
            'surface': surface,
            'rect': rect,
            'args': args,
            'position': None,
            'visible': self.surfaces[name]['visible']
        }
        self.surfaces[name]['position'] = UDim2(args['position'], self.surfaces[name]['surface'])