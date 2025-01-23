import pygame
import math
from bullet import Bullet
from spike import Spike

class Player:
    def __init__(self, x, y, width, length, speed, jump, color, rgb):
        self.vx = 0
        self.vy = 0
        self.x = x
        self.y = y
        self.width = width
        self.length = length
        self.speed = speed
        self.jump_force = jump
        self.jump_count = 0
        self.moving_x = False
        self.rect = pygame.Rect(x, y, width, length)
        self.health = 100
        if x < 950:
            self.going_right = True
        else:
            self.going_right = False
        self.color = (f"Player_{color}")
        self.rgb = rgb
        self.bullet_damage = 10  # Damage each bullet deals
        self.bullets = []  # List to store active bullets
        self.gun_length = 30
        self.gun_angle = 0
        
        

    def shoot(self, mouse_pos):
        gun_center = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        direction = pygame.math.Vector2(mouse_pos[0] - gun_center.x, mouse_pos[1] - gun_center.y).normalize()
        gun_barrel_x = gun_center.x + direction.x * self.gun_length
        gun_barrel_y = gun_center.y + direction.y * self.gun_length
        bullet = Bullet(gun_barrel_x, gun_barrel_y, direction, 500, self.bullet_damage, self.rgb)
        self.bullets.append(bullet)

    def update_bullets(self, dt, targets, gameObjects, screen):
        for bullet in self.bullets:
            if bullet.active:
                bullet.move(dt)
                for target in targets:
                    if bullet.is_lethal:
                        if bullet.check_collision(target):
                            target.damage(bullet.damage)  # Apply damage to the target
                    elif not bullet.check_collision(target):
                        bullet.is_lethal = True

                for object in gameObjects:
                    if not isinstance(object, Spike):
                        bullet.check_collision(object)
                bullet.render(screen)
            else:
                del bullet
                self.bullets = [bullet for bullet in self.bullets if bullet.active]
                print("yay")

    def move(self, dt, gameObjects):
        x_step = self.vx
        y_step = self.vy

        if self.vx < 0:
            self.going_right = False
        elif self.vx > 0:
            self.going_right = True

        collided = False

        # move position x
        self.rect.move_ip(x_step * dt, 0)

        for object in gameObjects:
            if not isinstance(object, Spike):
                if self.rect.colliderect(object):
                    self.rect.move_ip(-x_step * dt, 0)
                    self.vx = 0

        # move position y
        self.rect.move_ip(0, y_step * dt)

        if self.rect.y > 1000:
            self.damage(100)

        for object in gameObjects:
            if not isinstance(object, Spike):
                if self.rect.colliderect(object):
                    self.rect.move_ip(0, -y_step * dt)
                    if self.vy > 0:
                        self.vy = 0
                    elif self.vy < 0:
                        self.vy = 1

                    if self.rect.bottomright[1] != object.rect.topright[1]:
                        if self.rect.bottomright[1] < object.rect.topright[1]:
                            self.rect.move_ip(0, -(self.rect.bottomright[1] - object.rect.topright[1]))

        # handle spike collisions
        for obj in gameObjects:
            if isinstance(obj, Spike):
                if obj.handle_collision(self):  # Pass the Player object to the Spike
                    collided = True
        return collided

    def damage(self, amount):
        self.health -= amount

    def death(self):
        print("death")

    def render(self, screen, font, mouse_pos):
        # render the player
        if self.going_right:
            image = pygame.image.load(f"{self.color}\\Right.png").convert_alpha()
        elif not self.going_right:
            image = pygame.image.load(f"{self.color}\\Left.png").convert_alpha()
        scaled_image = pygame.transform.scale(image, (self.width, self.length))
        screen.blit(scaled_image, (self.rect))

        if mouse_pos[0] > self.rect.centerx:
            self.banana = pygame.transform.scale((pygame.image.load(f"gun\\Right.png").convert_alpha()),(60,60))
        else:
            self.banana = pygame.transform.scale((pygame.image.load(f"gun\\Left.png").convert_alpha()),(60,60))
        
        # calculate the gun angle
        gun_center = pygame.math.Vector2(self.rect.centerx, self.rect.centery)
        direction = pygame.math.Vector2(mouse_pos[0] - gun_center.x, mouse_pos[1] - gun_center.y)
        self.gun_angle = math.degrees(math.atan2(-direction.y, direction.x))

        # render the banana on top of the gun barrel
        rotated_banana = pygame.transform.rotate(self.banana, self.gun_angle)
        banana_rect = rotated_banana.get_rect(center=(gun_center.x, gun_center.y))
        screen.blit(rotated_banana, banana_rect.topleft)

        # render the arrow
        if self.rect.y < 0 - self.rect.height:
            arrow_y = 25
            arrow = pygame.image.load(f"{self.color}\\Arrow.png").convert_alpha()
            arrow = pygame.transform.scale(arrow, (40, 30))
            screen.blit(arrow, (self.rect.x + self.width / 2 - 20, arrow_y))

        # render the health and name
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.rect.x - 46, self.rect.y - 26, 152, 12))
        for h in range(self.health):
            pygame.draw.rect(screen, (self.rgb), pygame.Rect(self.rect.x + 1.5 * h - 45, self.rect.y - 25, 2, 10))