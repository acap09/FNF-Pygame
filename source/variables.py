import sys
from pathlib import Path

isEXE = getattr(sys, '_MEIPASS', False)
isExe = isEXE

if isExe:
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).parent.resolve()

mod_path = base_path / 'mods'
source_path = base_path / 'source'

running = True

curState = 'init'

screen = None
clock = None

registry = {}