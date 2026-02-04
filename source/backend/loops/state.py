import pygame
from source import variables
from source.functions.importfile import importModule

def findStateFile(name):
    name = str(name) + '.py'
    path = variables.source_path / 'states' / 'default' / name
    if path.exists():
        return path
    raise FileNotFoundError(f'File {name} not found in source/states/default')

def changeState(newState):
    filePath = None
    try:
        filePath = findStateFile(newState)
    except FileNotFoundError:
        return f'State could not be changed to {newState}'
