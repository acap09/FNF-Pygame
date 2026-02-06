import sys
from pathlib import Path
import pygame

isEXE = getattr(sys, '_MEIPASS', False)
isExe = isEXE

if isExe:
    base_path = Path(sys._MEIPASS)
else:
    base_path = Path(__file__).parent.parent.resolve()

mod_path = base_path / 'mods'
source_path = base_path / 'source'
temp_path = base_path / '_TEMP'
if not temp_path.exists():
    temp_path.mkdir()

running = True

curState = 'init'

screen: pygame.Surface = None
mainSurface: pygame.Surface = None
clock: pygame.time.Clock = None
sampleRate = pygame.mixer.get_init()[0]

aspectRatio = 16/9
invAspectRatio: float = 1/aspectRatio

registry = {}

elapsed = 0
dt = 0