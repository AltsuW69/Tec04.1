import pygame


class Bullet:
    def __init__(self, x, y, direction, speed, damage, color):
        self.x = x
        self.y = y
        self.direction = direction.normalize()  # Normalize the direction vector
        self.vx = self.direction.x * speed * 2
        self.vy = self.direction.y * speed * 4/3
        self.gravity = 500
        self.damage = damage
        self.radius = 5
        self.color = color
        self.active = True  # Bullet is active until it goes off-screen or hits something
        self.is_lethal = False


    def move(self, dt):
        self.vy += self.gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def render(self, screen):
        pygame.draw.circle(screen, (255,255,255) , (int(self.x), int(self.y)), self.radius +2)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


    def check_collision(self, target):
        if target.rect.collidepoint(self.x, self.y):  # Bullet hits the target
            if self.is_lethal:    
                self.active = False  # Deactivate the bullet
            return True
        return False