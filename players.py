import pygame

class Player:
    

    def __init__(self, x, y, width, length, speed, jump):
        self.vx = 0
        self.vy = 0
        self.width = width
        self.length = length
        self.speed = speed
        self.jump_force = jump
        self.double = False
        self.triple = False
        self.moving_x = False
        self.rect = pygame.Rect(x - width, y - length, width, length)


    def move(self, dt, gameObjects):
        x_step = self.vx
        y_step = self.vy
        
        collided = False
        
        self.rect.move_ip(x_step * dt, 0)
        
        for object in gameObjects:
            if self.rect.colliderect(object):
                self.rect.move_ip(-x_step * dt, 0)
                self.vx = 0
                if object.handle_collision():
                    collided = True
                
                
        
        self.rect.move_ip(0, y_step * dt)
        
        for object in gameObjects:
                if self.rect.colliderect(object):
                    self.rect.move_ip(0, -y_step * dt)
                    self.vy = 0
                    if object.handle_collision():
                        collided = True
                    
                    # ...
                    if self.rect.bottomright[1] != object.rect.topright[1]:
                        if self.rect.bottomright[1] < object.rect.topright[1]:
                            self.rect.move_ip(0, -(self.rect.bottomright[1] - object.rect.topright[1]))
        return collided
        
    
    def render(self, screen):
        image = pygame.image.load("Red_player.png").convert_alpha()
        scaled_image = pygame.transform.scale(image, (self.width, self.length))
        screen.blit(scaled_image, (self.rect))