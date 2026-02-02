import os
import sys
from pathlib import Path as PathLib

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
        # Base game path (inside exe or source folder)
        if getattr(sys, "_MEIPASS", False):
            base = PathLib(sys._MEIPASS)
        else:
            base = PathLib("..")

        # Mods folder always next to exe/script
        mods_path = PathLib(os.path.dirname(sys.argv[0])) / mods_folder

        # Check if mod exists
        mod_file = mods_path / filename
        base_file = base / filename

        if mod_file.exists():
            chosen = mod_file
        elif base_file.exists():
            chosen = base_file
        else:
            raise FileNotFoundError(filename)

        self = super().__new__(cls)
        self.path = chosen
        return self

    def __str__(self):
        return str(self.path)
