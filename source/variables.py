import sys
from pathlib import Path
import pygame
from source.classes.datatypes.Vector2 import Vector2

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

f11_path = base_path / 'screenshots'
if not f11_path.exists():
    f11_path.mkdir()
screenshot = False

running = True

curState = 'init'

screen: pygame.Surface = None
mainSurface: pygame.Surface = None
mainSurfaceSize: tuple = None
clock: pygame.time.Clock = None
sampleRate = pygame.mixer.get_init()[0]

aspectRatio = 16/9
invAspectRatio: float = 1/aspectRatio
fpsLimiter = 60

registry = {}

elapsed = 0
dt = 0

ALIGN_LL = '##LL##'
ALIGN_LC = '##LC##'
ALIGN_LR = '##LR##'
ALIGN_CL = '##CL##'
ALIGN_CC = '##CC##'
ALIGN_CR = '##CR##'
ALIGN_RL = '##RL##'
ALIGN_RC = '##RC##'
ALIGN_RR = '##RR##'

ALIGN_L = '##L##'
ALIGN_C = '##C##'
ALIGN_R = '##R##'

ALIGNMENTS_1D = [
    ALIGN_L, ALIGN_C, ALIGN_R
]
ALIGNMENTS_2D = [
    ALIGN_LL, ALIGN_LC, ALIGN_LR,
    ALIGN_CL, ALIGN_CC, ALIGN_CR,
    ALIGN_RL, ALIGN_RC, ALIGN_RR,
]