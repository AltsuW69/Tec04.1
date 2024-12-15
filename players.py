import pygame
from spike import Spike
class Player:
    

    def __init__(self, x, y, width, length, speed, jump, color):
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
        self.health = 100
        self.going_right = True
        self.color = color


    def move(self, dt, gameObjects):
        x_step = self.vx
        y_step = self.vy
        
        if self.vx < 0:
            self.going_right = False
        elif self.vx > 0:
            self.going_right = True

        collided = False

#move position x
        self.rect.move_ip(x_step * dt, 0)
        
        for object in gameObjects:
            if not isinstance(object, Spike):
                if self.rect.colliderect(object):
                    self.rect.move_ip(-x_step * dt, 0)
                    self.vx = 0

#move position y
        self.rect.move_ip(0, y_step * dt)
        
        for object in gameObjects:
            if not isinstance(object, Spike):
                if self.rect.colliderect(object):
                    self.rect.move_ip(0, -y_step * dt)
                    self.vy = 0

                    if self.rect.bottomright[1] != object.rect.topright[1]:
                        if self.rect.bottomright[1] < object.rect.topright[1]:
                            self.rect.move_ip(0, -(self.rect.bottomright[1] - object.rect.topright[1]))

#handle spike collisions
        for obj in gameObjects:
            if isinstance(obj, Spike):
                if obj.handle_collision(self):  # Pass the Player object to the Spike
                    collided = True
        return collided

    def damage(self,amount):
        self.health -= amount

    def death(self):
        print("death")
    
    def render(self, screen):
        if self.color == "red":    
            if self.going_right:
                image = pygame.image.load("Player_red\\Red_right.png").convert_alpha()
            elif not self.going_right:
                image = pygame.image.load("Player_red\\Red_left.png").convert_alpha()
        elif self.color == "blue":    
            if self.going_right:
                image = pygame.image.load("Player_blue\\Blue_right.png").convert_alpha()
            elif not self.going_right:
                image = pygame.image.load("Player_blue\\Blue_left.png").convert_alpha()
        
        
#        image = pygame.image.load("Red_player.png").convert_alpha()
        scaled_image = pygame.transform.scale(image, (self.width, self.length))
        screen.blit(scaled_image, (self.rect))