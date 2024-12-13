from typing import List
import pygame

from objects import Object
from spike import Spike
from players import Player

pygame.init()
screen = pygame.display.set_mode([1900, 900])


running = True
tick_count = 0
clock = pygame.time.Clock()

player = Player(100, 100, 40, 40, 200, 850)

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

    
print(gameObjects)


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


    player.move(dt, gameObjects)

    if not keys[pygame.K_a] and not keys[pygame.K_d]:
        player.moving_x = False
        
    if not player.moving_x:
        if player.vx > 0:
            player.vx -= 25
        
        if player.vx < 0:
            player.vx += 25
    
    if player.vy == 0:
        player.double = False
        player.triple = False
        
    player.render(screen)
    
    for g in gameObjects:
        g.render(screen)

    pygame.display.flip()



    tick_count += 1
pygame.quit()