import pygame
import random
from typing import List
from objects import Object
from spike import Spike
from players import Player
import os
pygame.init()

def cd_folder(folder_name):
    try:
        # Get the current working directory
        current_dir = os.getcwd()
        
        # Build the target path
        target_path = os.path.join(current_dir, folder_name)
        
        # Change to the target directory
        os.chdir(target_path)
        print(f"Switched to directory: {os.getcwd()}")
    except FileNotFoundError:
        print(f"Error: The folder '{folder_name}' does not exist in '{current_dir}'.")
    except PermissionError:
        print(f"Error: Permission denied to access the folder '{folder_name}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

cd_folder("ball_game")  # Change to "ball_game" folder in the current directory

screen = pygame.display.set_mode([1900, 900])
font = pygame.font.Font(None, 36)

# Game States
LOBBY, PLAYING, DEATH_SCREEN = "LOBBY", "PLAYING", "DEATH_SCREEN"
game_state = LOBBY

# Color Options and Resources
color_data = {
    "green": {"rgb": (5, 102, 57), "image": pygame.image.load("Player_green\\Arrow.png")},
    "red": {"rgb": (71, 0, 11), "image": pygame.image.load("Player_red\\Arrow.png")},
    "blue": {"rgb": (3, 104, 115), "image": pygame.image.load("Player_blue\\Arrow.png")},
    "yellow": {"rgb": (115, 90, 6), "image": pygame.image.load("Player_yellow\\Arrow.png")}
}
colors = list(color_data.keys())
color_rects = [pygame.Rect(500 + i * 250, 400, 200, 150) for i in range(4)]
selected_color = None

# Player and Game Objects
player = None
targets: List[Player] = []
gameObjects: List[Object] = []
stages = []

# Load the game map initially
def load_map():
    global gameObjects, x1,y0,x2, stage
    gameObjects.clear()
    gameObjects.append(Object(-10,-900,10,2000))
    gameObjects.append(Object(1900,-900,10,2000))
    if len(stages) == 0:
        for i in range(1,7):
            stages.append(i)
    stage = random.choice(stages) 
    stages.remove(stage)
    with open (f"stages\\stage{stage}.txt") as file:
        for line in file.readlines():
            data = line.rstrip().split(",")
            if len(data) == 3:
                x1 = int(data[0])
                x2 = int(data[1])
                y0 = int(data[2])
            if len(data) != 5:
                continue
            x = int(data[0])
            y = int(data[1])
            w = int(data[2])
            h = int(data[3])
            t = data[4]
            
            if t == "s":
                gameObjects.append(Spike(x, y, w, h))
            elif t == "p":
                gameObjects.append(Object(x, y, w, h))

# Runtime Variables
clock = pygame.time.Clock()
tick_count = 0
jump_time = 0
running = True
clicked = False
# Buttons
exit_button = pygame.Rect(800, 800, 300, 100)
return_to_lobby_button = pygame.Rect(800, 500, 300, 100)

def reset_game():
    global targets, tick_count, jump_time, game_state, selected_color
    targets.clear()
    selected_color = None
    tick_count = jump_time = 0
    game_state = LOBBY

# Main Game Loop
while running:
    dt = clock.tick(60) / 1000
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()

    # Quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # LOBBY SCREEN
    if game_state == LOBBY:
        screen.fill((255, 255, 255))

        # Render color selection
        for idx, rect in enumerate(color_rects):
            color = colors[idx]
            is_selected = selected_color == color

            # Toggle color selection
            if rect.collidepoint(mouse_pos) and mouse_click[0]:
                clicked = True
            if rect.collidepoint(mouse_pos) and clicked and not mouse_click[0]:
                clicked = False
                if is_selected:
                    selected_color = None  # De-select
                else:
                    selected_color = color

            # Render the rectangles with highlight for selection
            if selected_color == color:
                pygame.draw.rect(screen, (0, 0, 0), rect, 5)
            scaled_image = pygame.transform.scale(color_data[color]["image"], (200, 150))
            screen.blit(scaled_image, rect.topleft)

        # Render start button if a color is selected
        if selected_color:
            start_button = pygame.Rect(850, 700, 200, 80)
            hover = start_button.collidepoint(mouse_pos)
            button_color = color_data[selected_color]["rgb"]
            hover_color = tuple(min(255, c + 50) for c in button_color)
            
            if hover:
                pygame.draw.rect(screen, hover_color, start_button)
                if mouse_click[0]:
                    clicked = True
                if clicked and not mouse_click[0]:
                    clicked = False
                    load_map()
                    player = Player(x1, y0, 60, 60, 300, 850, selected_color, color_data[selected_color]["rgb"])   
                    targets.append(player)
                    game_state = PLAYING
            else:
                pygame.draw.rect(screen, button_color, start_button)
            start_text = font.render("START", True, (255, 255, 255))
            screen.blit(start_text, start_text.get_rect(center=start_button.center))



        # Exit Button
        if exit_button.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (0, 0, 0), exit_button)
            if mouse_click[0]: running = False
        else:
            pygame.draw.rect(screen, (0, 0, 0), exit_button)

        exit_text = font.render("EXIT", True, (255, 255, 255))
        screen.blit(exit_text, exit_text.get_rect(center=exit_button.center))

        pygame.display.flip()

    # GAMEPLAY
    elif game_state == PLAYING:
        keys = pygame.key.get_pressed()
        click = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        # Player input
        if click[0] and not clicked:
            clicked = True 
        elif not click[0] and clicked:
            clicked = False  # Reset the clicking state
            player.shoot(mouse_pos)
        if click[2]:
            #player.death()
            #game_state = DEATH_SCREEN
            player.shoot(mouse_pos)

        if keys[pygame.K_w] and player.jump_count < 2 and tick_count - jump_time > 10 or keys[pygame.K_SPACE] and player.jump_count < 2 and tick_count - jump_time > 20:
            player.vy = -player.jump_force
            jump_time = tick_count
            player.jump_count += 1
        if keys[pygame.K_a]:
            player.moving_x = True
            player.vx = -player.speed
        if keys[pygame.K_d]:
            player.moving_x = True
            player.vx = player.speed

        # Update player and check damage
        player.vy += 30

        if player.move(dt, gameObjects):
            player.damage(1)

        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            player.moving_x = False

        if not player.moving_x:
            if player.vx > 0:
                player.vx -= 25
            elif player.vx < 0:
                player.vx += 25

        # Check player death
        if player.health <= 0:
            player.death()
            game_state = DEATH_SCREEN

        if player.vy == 0:
            player.jump_count = 0

        # Render Gameplay
        image = pygame.image.load("forest.png").convert_alpha()
        image = pygame.transform.scale(image, (1900, 900))
        screen.blit(image, (0, 0))
        for g in gameObjects: 
            g.render(screen)
        text_surface = font.render(str(stage), True, (200, 255, 255))
        screen.blit(text_surface, (15, 10))

        player.render(screen, font, mouse_pos)
        player.update_bullets(dt, targets, gameObjects, screen)
        pygame.display.flip()
        tick_count += 1

    # DEATH SCREEN
    elif game_state == DEATH_SCREEN:
        screen.fill((0, 0, 0))
        death_text = font.render("You Died!", True, (255, 0, 0))
        screen.blit(death_text, death_text.get_rect(center=(950, 400)))

        pygame.draw.rect(screen, (0, 0, 200), return_to_lobby_button)
        return_text = font.render("RETURN TO LOBBY", True, (255, 255, 255))
        screen.blit(return_text, return_text.get_rect(center=return_to_lobby_button.center))

        # Button behavior
        if return_to_lobby_button.collidepoint(mouse_pos) and mouse_click[0]:
            reset_game()
        pygame.display.flip()

pygame.quit()