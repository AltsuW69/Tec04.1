import pygame
import random

class Object:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.picture = pygame.Surface((self.w, self.h))
        for y in range(self.h):
            for x in range(self.w):
                gray = random.randint(0, 50)  # Base stone color
                moss = random.randint(50, 100)   # Moss effect
                r = gray  # Red channel for stone base
                g = moss
                b = gray  # Blue channel for stone
                self.picture.set_at((x, y), (r, g, b))

    def handle_collision(self):
        return False 

    def render(self, screen):
        # Render the pre-generated texture to the screen
        screen.blit(self.picture, (self.x, self.y))