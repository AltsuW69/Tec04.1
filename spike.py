import pygame
from objects import Object

class Spike(Object):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

    def render(self, screen):
        pygame.draw.rect(screen, (150, 30, 0), self.rect)