#import the needed libraries etc.
import pygame
from characters import Character
from objects import Object
pygame.init()


#define attributes
screen_width = 1800
screen_length = 900
running = True
clock = pygame.time.Clock()
player_speed = 300
x1 = screen_width/4
y1 = screen_length/2
x2 = screen_width/4*3
y2 = screen_length/2
player_radius = 25
ground_length = 60
platform_lenght = 60
platform_width = screen_width/7
fall_force1 = 0
fall_force2 = 0
double_check1 = False
double_check2 = False
triple_check1 = False
triple_check2 = False

#create objects
screen = pygame.display.set_mode([screen_width, screen_length])
player1 = Character(x1, y1, player_radius, player_speed)
player2 = Character(x2, y2, player_radius, player_speed)
ground = Object(screen_width, screen_length - ground_length/2, 0, screen_length - ground_length)
platform_1 = Object(platform_width, platform_lenght, screen_width/5 - platform_width/2, screen_length/20*13 - platform_lenght/2)
platform_2 = Object(platform_width, platform_lenght, screen_width/5*4  - platform_width/2, screen_length/20*13 - platform_lenght/2)

tick_count = 0

#makes sure that the program stops when the game is closed
while running:
    dt = clock.tick(60)/1000
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#rectangle hitboxes
    circle1_hitbox = pygame.Rect(player1.position_x - player1.size, player1.position_y - player1.size, player1.size * 2, player1.size * 2)
    pygame.draw.rect(screen, (0, 0, 255), circle1_hitbox, 2)
    circle2_hitbox = pygame.Rect(player2.position_x - player2.size, player2.position_y - player2.size, player2.size * 2, player2.size * 2)
    pygame.draw.rect(screen, (0, 0, 255), circle2_hitbox, 2)
    ground_hitbox = pygame.Rect(ground.x, ground.y, ground.width, ground.length)
    platform1_hitbox = pygame.Rect(platform_1.x, platform_1.y, platform_1.width, platform_1.length)
    platform2_hitbox = pygame.Rect(platform_2.x, platform_2.y, platform_2.width, platform_2.length)



#rendering
    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (20, 113, 160), (player1.position_x, player1.position_y), player1.size)
    pygame.draw.circle(screen, (166, 26, 26), (player2.position_x, player2.position_y), player2.size)
    pygame.draw.rect(screen, (102, 48, 11), (ground.x, ground.y, ground.width, ground.length), 0)
    pygame.draw.rect(screen, (102, 48, 11), (platform1_hitbox), 0)
    pygame.draw.rect(screen, (102, 48, 11), (platform2_hitbox), 0)
    pygame.display.flip()


#dont allow colliding with other players
    if circle1_hitbox.colliderect(circle2_hitbox) or circle2_hitbox.colliderect(circle1_hitbox):
        
        if keys[pygame.K_d] or keys[pygame.K_a]:
            if player1.position_x + player1.size > player2.position_x - player2.size and player1.position_x < player2.position_x:
                if not player1.position_y + player1.size < player2.position_y and not player1.position_y - player1.size > player2.position_y:
                    player1.position_x = player2.position_x - player2.size - player1.size - 5
            if player1.position_x - player1.size < player2.position_x + player2.size and player1.position_x > player2.position_x:
                if not player1.position_y + player1.size < player2.position_y and not player1.position_y - player1.size > player2.position_y:    
                    player1.position_x = player2.position_x + player2.size + player1.size + 5

        if keys[pygame.K_l] or keys[pygame.K_j]:
            if player2.position_x + player2.size > player1.position_x - player1.size and player2.position_x < player1.position_x:
                if not player2.position_y + player2.size < player1.position_y and not player2.position_y - player2.size > player1.position_y:    
                    player2.position_x = player1.position_x - player1.size - player2.size - 5
            if player2.position_x - player2.size < player1.position_x + player1.size and player2.position_x > player1.position_x:
                if not player2.position_y + player2.size < player1.position_y and not player2.position_y - player2.size > player1.position_y:   
                    player2.position_x = player1.position_x + player2.size + player2.size + 5

        if player1.position_y + player1.size > player2.position_y - player2.size and player1.position_y < player2.position_y:
            player1.position_y = player2.position_y - player2.size - player1.size
            fall_force1 = 0
            if fall_force2 < 0:
                fall_force2 = 20
            double_check1 = False
            triple_check1 = False
        
        if player2.position_y + player2.size > player1.position_y - player1.size and player2.position_y < player1.position_y:
            player2.position_y = player1.position_y - player1.size - player2.size
            fall_force2 = 0
            if fall_force1 < 0:
                fall_force1 = 20
            double_check2 = False
            triple_check2 = False


#player 1 movement

    #left/right
  
    if player1.position_x + player1.size < screen_width:
        if keys[pygame.K_d]:
            player1.move_player_x(1, dt)
            
    if player1.position_x - player1.size > 0:
        if keys[pygame.K_a]:
            player1.move_player_x(-1, dt)
            


    #fall
    if not circle1_hitbox.colliderect(ground_hitbox):
        player1.position_y += fall_force1 * dt
        fall_force1 += 20
    elif circle1_hitbox.colliderect(ground_hitbox):
        fall_force1 = 0
        double_check1 = False
        triple_check1 = False
        if player1.position_y + player1.size < ground.length:
            player1.position_y = ground.y - player1.size


    #jump
    if circle1_hitbox.colliderect(ground_hitbox) or not triple_check1:
        if keys[pygame.K_w] and not double_check1:
            fall_force1 = -700
            player1.position_y += fall_force1 * dt
            double_check1 = True
            jump_time1 = tick_count
        elif keys[pygame.K_w] and tick_count - jump_time1 > 20:
            fall_force1 = -500
            player1.position_y += fall_force1 * dt
            triple_check1 = True

    


#player 2 movement    
        
    #left/right   
    if player2.position_x + player2.size < screen_width:
        if keys[pygame.K_l]:
            player2.move_player_x(1, dt)
    if player2.position_x - player2.size > 0:
        if keys[pygame.K_j]:
            player2.move_player_x(-1, dt)


    #fall
    if not circle2_hitbox.colliderect(ground_hitbox):
        player2.position_y += fall_force2 * dt
        fall_force2 += 20
    elif circle2_hitbox.colliderect(ground_hitbox):
        fall_force2 = 0
        double_check2 = False
        triple_check2 = False
        player2.position_y = ground.y - player2.size

    #jump
    if circle2_hitbox.colliderect(ground_hitbox) or not triple_check2:
        if keys[pygame.K_i] and not double_check2:
            fall_force2 = -700
            player2.position_y += fall_force2 * dt
            double_check2 = True
            jump_time2 = tick_count
        elif keys[pygame.K_i] and tick_count - jump_time2 > 20:
            fall_force2 = -500
            player2.position_y += fall_force2 * dt
            triple_check2 = True

    


    tick_count += 1
pygame.quit()