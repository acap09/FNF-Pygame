import source.variables as v
import pathlib as pl

#class Path:
#    def __new__(cls, relativePath):
#        basePath = os.path.abspath('.')
#        if getattr(sys, '_MEIPASS', False):
#            basePath = sys._MEIPASS
#
#        fullPath = os.path.join(basePath, relativePath)
#
#        if not os.path.exists(fullPath):
#            raise FileNotFoundError(fullPath)
#
#        self  = super().__new__(cls)
#        self.path = PathLib(fullPath)
#        return self
#
#    def __str__(self):
#        return str(self.path)

class Path:
    def __new__(cls, filename, mods_folder="mods"):
        if isinstance(filename, Path):
            filename = filename.path
        mod_file = v.mod_path / filename
        base_file = v.source_path / filename
        if mod_file.exists():
            file = mod_file
        elif base_file.exists():
            file = base_file
        else:
            raise FileNotFoundError(filename)

        self = super().__new__(cls)
        self.path = file
        return self

    def __str__(self):
        return str(self.path)
    g = __str__

    def __repr__(self):
        return f'<Path {self.path}>'

    def __truediv__(self, other):
        if isinstance(other, (pl.Path, str)):
            return self.path / other
        elif isinstance(other, Path):
            return self.path / other.path
        raise TypeError(f'unsupported operand type(s) for /: \'{type(self)}\' and \'{type(other)}\'')
