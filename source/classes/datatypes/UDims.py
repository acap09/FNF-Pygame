# Going the Roblox path
import source.variables as v
#from source.classes.datatypes.Vector2 import Vector2
import pygame
from source.classes.datatypes.Vector2 import Vector2
import warnings

class UserInterfaceDimension:
    def __init__(self, scale: float = 0.0, offset: int = 0):
        self.scale = scale
        self.offset = offset

    def tuple(self):
        return (self.scale, self.offset)

    def absPos(self, axis: str = 'x', Surface: pygame.Surface = v.mainSurface):
        #Surface = Surface if isinstance(Surface, pygame.Surface) else v.mainSurface
        #dim = (Surface.get_width(), Surface.get_height())
        Surface = v.mainSurface
        dim = v.mainSurfaceSize
        if isinstance(Surface, pygame.Surface):
            dim = Surface.get_size()
        #print('v.mainSurface', dim)
        axes = {'x': 0, 'y':1}
        if axis not in axes:
            raise ValueError(f'Axis {axis} not supported.')
        return self.scale * dim[axes[axis]] + self.offset

    def __repr__(self):
        return f'<UserInterfaceDimension s{self.scale} o{self.offset}>'
UDim = UserInterfaceDimension
#print(type(UDim(0, 0)))

class UserInterfaceDimension2:
    def __init__(self, arg1: UDim | float | tuple | str = None, arg2: UDim | int | tuple | pygame.Surface =
    None, arg3: float = None, arg4: int = None):
        if isinstance(arg1, UDim2):
            self.x = arg1.x
            self.y = arg1.y
            warnings.warn(f'Received a UDim2 object {arg1}. No changes will occur!')
            return

        if arg1 in v.ALIGNMENTS_2D:
            if not isinstance(arg2, pygame.Surface):
                raise TypeError(f'UDim2 alignment requires a Surface to be provided. Instead, we received '
                                f'{arg2 if arg2 is not None else 'nothing'}.')
            print(arg2.get_size(), arg1)
            conv = [UDim(), UDim()]
            for dim, align_dim in enumerate([arg1[2], arg1[3]]):
                if align_dim == 'L': #left
                    pass # already UDim(0, 0)
                elif align_dim == 'C':
                    conv[dim] = UDim(0.5, -int(arg2.get_size()[dim]/2))
                elif align_dim == 'R':
                    conv[dim] = UDim(0.5, -arg2.get_size()[dim])
            self.x = conv[0]
            self.y = conv[1]
            print(self, self.absPos())
            return


        datatypes = [arg1, arg2, arg3, arg4]
        args = [arg1, arg2, arg3, arg4]
        #maxArgs = sum(datatype is not None for datatype in datatypes)
        for n, val in enumerate(args):
            if isinstance(val, UDim) and n < 2:
                datatypes[n] = 'UDim'
            elif isinstance(val, tuple) and n < 2:
                datatypes[n] = 'tuple'
            elif isinstance(val, (float, int)):
                datatypes[n] = 'number'
            elif val is None:
                datatypes[n] = 'None'
            else:
                raise TypeError(f'arg{n+1} ({args[n]}) is not a valid type ({type(args[n])}!')

        constructor_map = {
            ('UDim', 'UDim'): lambda: (arg1, arg2),
            ('tuple', 'tuple'): lambda: (UDim(*arg1), UDim(*arg2)),
            ('number', 'number', 'number', 'number'): lambda: (UDim(arg1, arg2), UDim(arg3, arg4)),
            ('None', 'None', 'None', 'None'): lambda: (UDim(0, 0), UDim(0, 0))
        }

        key = tuple(datatypes)
        if key in constructor_map:
            self.x, self.y = constructor_map[key]()
        else:
            raise TypeError('Unsupported argument combination!')
        # what even is this bro 😭


    def tuple(self):
        return (self.x, self.y)

    def absPos(self, Surface: pygame.Surface = v.mainSurface, tupleify: bool = False):
        Surface = Surface if isinstance(Surface, pygame.Surface) else v.mainSurface

        ret = Vector2(self.x.absPos('x', Surface), self.y.absPos('y', Surface))
        if tupleify:
            ret = ret.tuple()
        return ret

    def __str__(self):
        return f'({self.x.scale}/{self.x.offset}, {self.y.scale}/{self.y.offset})'

    def __repr__(self):
        return f'<UserInterfaceDimension2 x(s{self.x.scale} o{self.x.offset}) y(s{self.y.scale} o{self.y.offset})>'
UDim2 = UserInterfaceDimension2