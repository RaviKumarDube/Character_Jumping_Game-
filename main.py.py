import pygame
import random
pygame.init()

# Window setup
game_window = pygame.display.set_mode((600, 500))
pygame.display.set_caption("Jumping Character Game")

# Load and scale background + character
Background_image = pygame.image.load('bg_image.jpeg')
Background_image = pygame.transform.scale(Background_image, (600, 500))

character_image = pygame.image.load('character.png')
character_image = pygame.transform.scale(character_image, (50, 50))

# Character setup
character_x = 100
character_y = 355
character_size = 50
velocity_x = 0
velocity_y = 0
gravity = 1
jump_power = -15
on_ground = True

# Obstacle setup
red = (255, 0, 0)
obstacles = []
spawn_time = 2000
last_spawn = pygame.time.get_ticks()
obstacle_speed = 5

# Score
score = 0
font = pygame.font.SysFont(None, 40)

fps = 60
clock = pygame.time.Clock()
running = True
game_over = False


def reset_game():
    """Restart game state"""
    global character_x, character_y, velocity_x, velocity_y, on_ground
    global obstacles, score, game_over, last_spawn

    character_x = 100
    character_y = 355
    velocity_x = 0
    velocity_y = 0
    on_ground = True
    obstacles = []
    score = 0
    game_over = False
    last_spawn = pygame.time.get_ticks()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            # controls only if alive
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and on_ground:
                    velocity_y = jump_power
                    on_ground = False
                if event.key == pygame.K_RIGHT:
                    velocity_x = 5
                if event.key == pygame.K_LEFT:
                    velocity_x = -5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    velocity_x = 0
        else:
            # restart when R is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()

    if not game_over:
        # apply gravity
        velocity_y += gravity
        character_y += velocity_y
        character_x += velocity_x

        # ground collision
        if character_y >= 355:
            character_y = 355
            velocity_y = 0
            on_ground = True

        # boundaries
        if character_x < 0:
            character_x = 0
        if character_x > 600 - character_size:
            character_x = 600 - character_size

        # spawn new obstacle every 2 sec
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn > spawn_time:
            box_y = 355
            box_size = 30
            obstacles.append([600, box_y, box_size])
            last_spawn = current_time

        # move obstacles left
        for box in obstacles:
            box[0] -= obstacle_speed

        # remove obstacles off-screen and add score
        new_obstacles = []
        for box in obstacles:
            if box[0] + box[2] > 0:
                new_obstacles.append(box)
            else:
                score += 10
        obstacles = new_obstacles

        # collision detection
        character_rect = pygame.Rect(character_x, character_y, character_size, character_size)
        for box in obstacles:
            box_rect = pygame.Rect(box[0], box[1], box[2], box[2])
            if character_rect.colliderect(box_rect):
                game_over = True

    # draw
    game_window.blit(Background_image, (0, 0))
    for box in obstacles:
        pygame.draw.rect(game_window, red, (box[0], box[1], box[2], box[2]))
    game_window.blit(character_image, (character_x, character_y))

    # show score
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    game_window.blit(score_text, (10, 10))

    # show game over
    if game_over:
        over_text = font.render("GAME OVER!", True, (255, 0, 0))
        restart_text = font.render("Press R to Restart", True, (0, 0, 0))
        game_window.blit(over_text, (200, 200))
        game_window.blit(restart_text, (180, 250))

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
