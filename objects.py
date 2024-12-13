import pygame



class Object():
    
    
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        
    def handle_collision(self):
        return False 
        
    def render(self, screen):
        pygame.draw.rect(screen, (80, 48, 15), self.rect)