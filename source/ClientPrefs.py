import pygame as pg

aspectRatio = 16/9
invAspectRatio: float = 1/aspectRatio
fpsLimiter = 60

class Keybinds:
    def __init__(self):
        self.enter = pg.K_RETURN

keybinds = Keybinds()
kb = keybinds