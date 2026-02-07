import pygame
from source import variables as v
import source.registry as reg
from source.functions.file_funcs import importModule
from path import Path
import warnings
oldState = None
curState = None


def findStateFile(name):
    name = str(name) + '.py'
    path = v.source_path / 'states' / name
    if path.exists():
        return path
    raise FileNotFoundError(f'File {path} not found in source/states/!')
#curState = importModule(findStateFile('init'))

def changeState(newState: str):
    print('hi!!!')
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
    reg.add('States', curState.__name__, curState)

changeState('init')


def update():
    if hasattr(curState, 'updatePre') and callable(curState.updatePre):
        curState.updatePre()

    if hasattr(curState, 'updatePost') and callable(curState.updatePost):
        curState.updatePost()