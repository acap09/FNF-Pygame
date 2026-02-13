import pygame

class Surface(pygame.Surface):
    def __init__(self, size, flags=0, depth=0, masks=None):
        super().__init__(size, flags, depth, masks)

    def recolor(self, color):
        surf = pygame.Surface(self.get_size())
        surf.fill(color)
        self.blit(surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)