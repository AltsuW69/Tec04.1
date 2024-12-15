from typing import List
import pygame

from objects import Object
from spike import Spike
from players import Player

pygame.init()
screen = pygame.display.set_mode([1900, 900])
font = pygame.font.Font(None, 36)

running = True
tick_count = 0
damage_time = 0
clock = pygame.time.Clock()

player = Player(100, 100, 40, 40, 300, 850, "blue")

gameObjects: List[Object] = []

file = open("stage1.txt")
for line in file.readlines():
    data = line.rstrip().split(",")
    
    if len(data) != 5:
        print("Invalid line: " + line)
        continue
    
    x = int(data[0])
    y = int(data[1])
    w = int(data[2])
    h = int(data[3])
    
    # Type of the gameObject
    t = data[4]
    
    if t == "s":
        new_spike = Spike(x, y, w, h)
        gameObjects.append(new_spike)
    elif t == "p":
        new_gameobject = Object(x, y, w, h)
        gameObjects.append(new_gameobject)


while running:
    # Aika edellisestä näytön päivityksestä (deltaTime)
    dt = clock.tick(60)/1000
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not player.triple:
        if keys[pygame.K_w] and not player.double:
            player.vy = -player.jump_force
            jump_time = tick_count
            player.double = True
        if keys[pygame.K_w] and tick_count - jump_time > 20:
            player.vy = -player.jump_force
            player.triple = True
    if keys[pygame.K_a]:
        player.moving_x = True
        player.vx = -player.speed
    if keys[pygame.K_d]:
        player.moving_x = True
        player.vx = player.speed

    image = pygame.image.load("forest.png").convert_alpha()
    image = pygame.transform.scale(image, (1900, 900))
    screen.fill((255, 255, 255))
    screen.blit(image, (0, 0))

    player.vy += 30

    spike_check = player.move(dt, gameObjects)
    if spike_check and tick_count - damage_time > 2:

        damage_time = tick_count
        player.damage(1)



    if not keys[pygame.K_a] and not keys[pygame.K_d]:
        player.moving_x = False
        
    if not player.moving_x:
        if player.vx > 0:
            player.vx -= 25
        
        if player.vx < 0:
            player.vx += 25
    
    if player.health <= 0:
        player.death()
        running = False

    if player.vy == 0:
        player.double = False
        player.triple = False

#render stuff
    for g in gameObjects:
        g.render(screen)
    
    player.render(screen)
    
    text_surface = font.render(str(f"Health:{player.health}"), True, (0, 0, 0))
    screen.blit(text_surface, (15, 10))
    
    pygame.display.flip()


    tick_count += 1
pygame.quit()