import pygame
from objects import Object

class Spike(Object):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        pyramid_height = w / 2  # Total pyramid height is half the base width
        num_levels = 4  # Number of rows in the pyramid
        rect_height = pyramid_height / num_levels  # Height of each rectangle

        self.rects = []
        for i in range(num_levels):
            # Calculate the width of the current level
            row_width = w * (1 - (i / num_levels))
            # Center the row horizontally
            row_x = x + (w - row_width) / 2
            # Position the row above the base
            row_y = y - (rect_height * (i + 1))
            # Add the rectangle for this level
            self.rects.append(pygame.Rect(row_x, row_y, row_width, rect_height))
            # Calculate the width of the current level
            row_width = w * (1 - (i / num_levels))
            # Center the row horizontally
            row_x = x + (w - row_width) / 2
            # Position the row below the base (invert the logic)
            row_y = y + (rect_height * i)
            # Add the rectangle for this level
            self.rects.append(pygame.Rect(row_x, row_y, row_width, rect_height))


        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.pictures = []
        i1 = pygame.image.load("sawblade_images\\sawblade.png").convert_alpha()
        i1 = pygame.transform.scale(i1, (w, w))
        self.pictures.append(i1)
        i2 = pygame.image.load("sawblade_images\\sawblade1.png").convert_alpha()
        i2 = pygame.transform.scale(i2, (w, w))
        self.pictures.append(i2)
        i3 = pygame.image.load("sawblade_images\\sawblade2.png").convert_alpha()
        i3 = pygame.transform.scale(i3, (w, w))
        self.pictures.append(i3)
        i4 = pygame.image.load("sawblade_images\\sawblade3.png").convert_alpha()
        i4 = pygame.transform.scale(i4, (w, w))
        self.pictures.append(i4)
        i5 = pygame.image.load("sawblade_images\\sawblade4.png").convert_alpha()
        i5 = pygame.transform.scale(i5, (w, w))
        self.pictures.append(i5)

        self.animation_index = 0
        self.animation_timer = 0


    def handle_collision(self, player):
        for rect in self.rects:
            if player.rect.colliderect(rect):  
                return True 
    
    def render(self, screen):
#        pygame.draw.rect(screen, (150, 30, 0), self.rect)
#        for rect in self.rects:
 #           pygame.draw.rect(screen, (150, 30, 0), rect)
        self.animation_timer += 1

        if self.animation_timer >= 5:
            self.animation_index = (self.animation_index + 1) % len(self.pictures)
            self.animation_timer = 0

        # Draw the current animation frame
        screen.blit(self.pictures[self.animation_index], (self.x, self.y - self.w / 2, self.w, self.h))