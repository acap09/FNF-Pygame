import pygame
from source import variables as v
import source.registry as reg
from source.functions.file_funcs import importModule
from source.classes.extend.Image import Image
from source.classes.datatypes.UDims import UDim2
from source.classes.base.Tween import Tween
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
cs = change_state

#transSurf = pygame.Surface(v.mainSurfaceSize, pygame.SRCALPHA)
transition = Image('transState', 'images/transition/fadebig.png')
transition.visible = False
transTween = Tween('transitionState', transition, 'position', UDim2(0, 0, -0.25, 0), 1, 'easeOutCubic')
def change_state_transition1(newState: str, skipTrans2: bool = False):
    transition.visible = True
    transition.resize(None, UDim2(1002/1000, 0, 844/562.5, 0))
    transTween.stop()
    transition.position = UDim2(0, 0, -1, 0)
    transition.flip(False, False)
    #print('are you okay')
    transTween.play()
    transTween.on_complete_args = [newState, skipTrans2]
    transTween.on_complete = change_state_transition2
change_state_transition = change_state_transition1
cst = change_state_transition1

def change_state_transition2(newState: str, skip_me: bool = False):
    global transTween
    change_state(newState)
    if skip_me:
        transition.visible = False
        return
    transTween = Tween('transitionStateIn', transition, 'position', UDim2(0, 0, 1, 0), 1, 'easeOutCubic')
    transTween.play()
    transTween.on_complete = lambda: None

change_state('init')

def updatePre():
    if hasattr(curState, 'updatePre') and callable(curState.updatePre):
        curState.updatePre()

def update():
    if hasattr(curState, 'update') and callable(curState.update):
        curState.update()
    transition.update_size()

    if hasattr(curState, 'updatePost') and callable(curState.updatePost):
        curState.updatePost()

def windowResize(dim):
    pass

def render():
    if transition.visible:
        v.mainSurface.blit(transition.img, transition.position.absPos(tupleify=True))