import pygame
from source import variables as v
import source.registry as reg
from source.functions.file_funcs import importModule
from path import Path
import warnings
oldState = None
curState = None


def find_state_file(name):
    name = str(name) + '.py'
    path = v.source_path / 'states' / name
    if path.exists():
        return path
    raise FileNotFoundError(f'File {path} not found in source/states/!')
#curState = importModule(findStateFile('init'))

def change_state(newState: str):
    #print('hi!!!')
    global oldState, curState
    filePath = None
    try:
        filePath = Path(f'states/{newState}.py').path
    except FileNotFoundError:
        warnings.warn(f'State could not be changed to {newState}')
        return f'State could not be changed to {newState}'

    if hasattr(curState, 'onDestroy') and callable(curState.onDestroy):
        curState.onDestroy(newState)
        reg.remove('States', curState.__name__)
    oldState = curState
    curState = importModule(filePath)
    v.curState = newState
    reg.add('States', curState.__name__, curState)

transSurf = pygame.Surface((800, 600), pygame.SRCALPHA)
fade = pygame.image.load(Path('images/transition/fade.png').path)
def change_state_transition(newState: str):
    global transSurf
    transSurf.fill((0, 0, 0, 0))
    transSurf = pygame.transform.scale(transSurf, v.mainSurfaceSize)
    pygame.draw.rect(transSurf, (0, 0, 0), pygame.Rect(0, 0, transSurf.get_width(), int(transSurf.get_height()*0.75)))
    transSurf.set_alpha(255)
    transSurf.blit(pygame.transform.scale(fade, (transSurf.get_width(), int(transSurf.get_height()*0.25))),
                   (0, int(transSurf.get_height()*0.75)))

change_state('init')

def updatePre():
    if hasattr(curState, 'updatePre') and callable(curState.updatePre):
        curState.updatePre()

def update():
    if hasattr(curState, 'update') and callable(curState.update):
        curState.update()

    if hasattr(curState, 'updatePost') and callable(curState.updatePost):
        curState.updatePost()

def render():
    v.mainSurface.blit(transSurf, (0, 0))