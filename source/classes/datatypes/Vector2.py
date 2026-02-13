import pygame#_ce

class Vector2(pygame.math.Vector2):
    def __init__(self, a1=0, a2=0):
        super().__init__(a1, a2)

    def tuple(self):
        return (self.x, self.y)