# Going the Roblox path
import source.variables as v
#from source.classes.datatypes.Vector2 import Vector2
import pygame
from source.classes.datatypes.Vector2 import Vector2
import warnings

class UserInterfaceDimension:
    def __init__(self, scale: float, offset: int):
        self.scale = scale
        self.offset = offset

    def tuple(self):
        return (self.scale, self.offset)

    def absPos(self, axis: str = 'x', Surface: pygame.Surface = v.mainSurface):
        Surface = Surface if isinstance(Surface, pygame.Surface) else v.mainSurface
        dim = Surface.get_size()
        axes = {'x': 0, 'y':1}
        if axis not in axes:
            raise ValueError(f'Axis {axis} not supported.')
        return self.scale * dim[axes[axis]] + self.offset

    def __repr__(self):
        return f'<UserInterfaceDimension s{self.scale} o{self.offset}>'
UDim = UserInterfaceDimension
print(type(UDim(0, 0)))

class UserInterfaceDimension2:
    def __init__(self, arg1: UDim | float | tuple = None, arg2: UDim | int | tuple = None, arg3: float = None,
                 arg4: int = None):
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

        if datatypes[0] == 'UDim' and datatypes[1] == 'UDim':
            self.x = arg1
            self.y = arg2
        elif datatypes[0] == 'tuple' and datatypes[1] == 'tuple':
            self.x = UDim(arg1[0], arg1[1])
            self.y = UDim(arg2[0], arg2[1])
        elif datatypes[0] == 'number' and datatypes[1] == 'number' and datatypes[2] == 'number' and datatypes[3] == 'number':
            self.x = UDim(float(arg1), int(arg2))
            self.y = UDim(float(arg3), int(arg4))
        elif datatypes[0] == 'None' and datatypes[1] == 'None' and datatypes[2] == 'None' and datatypes[3] == 'None':
            self.x = UDim(0, 0)
            self.y = UDim(0, 0)
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