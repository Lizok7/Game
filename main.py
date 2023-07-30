import pygame
import random
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 20)
FONT_1 = pygame.font.SysFont('Verdana', 100)

COLOR_BLUE = (0, 0, 255)
COLOR_GREY = (128, 128, 128)
COLOR_YELLOW = (255, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_x1 = 0
bg_x2 = bg.get_width()
bg_move = 4

IMAGE_PATH = "goose"
PLAYER_IMG = os.listdir(IMAGE_PATH)

player_size = (20, 20)
main_display = pygame.display.set_mode((WIDTH, HEIGHT))
player = pygame.image.load('player.png').convert_alpha()

bonus_size = (20, 20)
bonus_speed = 4

initial_player_x = WIDTH // 4
initial_player_y = HEIGHT // 2

player_rect = player.get_rect()
player_rect.topleft = (initial_player_x, initial_player_y)
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_up = [0, -4]
player_move_left = [-4, 0]

MAX_BONUSES = 15
MAX_ENEMIES = 30

bonuses = []
enemies = []
rockets = []

def create_enemy():
    enemy_size = (30, 30)
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_rect = enemy.get_rect(center=(WIDTH, random.randint(enemy_size[1] // 2, HEIGHT - enemy_size[1] // 2)))
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_rect = bonus.get_rect(center=(random.randint(bonus_size[0] // 2, WIDTH - bonus_size[0] // 2), -bonus_size[1] // 2))
    bonus_move = [0, random.randint(4, 8)]
    return [bonus, bonus_rect, bonus_move]

def create_rocket():
    rocket = pygame.image.load('rocket.png').convert_alpha()
    rocket_rect = pygame.Rect(player_rect.x + player_rect.width, player_rect.y + player_rect.height // 2, 20, 10)
    rocket_move = [8, 0]
    return [rocket, rocket_rect, rocket_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)
CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 200)

score = 0
image_index = 0
inscription = "Game over"
game_over = False
speed_multiplier = 1

playing = True
while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        elif event.type == CREATE_ENEMY and len(enemies) < MAX_ENEMIES:
            enemies.append(create_enemy())
        elif event.type == CREATE_BONUS and len(bonuses) < MAX_BONUSES:
            bonuses.append(create_bonus())
        elif event.type == CHANGE_IMG:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMG[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMG):
                image_index = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                rockets.append(create_rocket())

    bg_x1 -= bg_move * speed_multiplier
    bg_x2 -= bg_move * speed_multiplier

    main_display.blit(bg, (bg_x1, 0))
    main_display.blit(bg, (bg_x2, 0))

    if bg_x1 < -bg.get_width():
        bg_x1 = bg.get_width()

    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if enemy[1].right < 0:
            enemies.remove(enemy)

        if player_rect.colliderect(enemy[1]):
            playing = False
            game_over = True

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if bonus[1].top > HEIGHT:
            bonuses.remove(bonus)

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.remove(bonus)

    for rocket in rockets:
        rocket[1] = rocket[1].move(rocket[2])
        main_display.blit(rocket[0], rocket[1])

        if rocket[1].right > WIDTH:  
            rockets.remove(rocket)

    if score >= 5:
        speed_multiplier = 2 

    if game_over:
        main_display.blit(FONT_1.render("Game over", True, COLOR_RED), (WIDTH // 2 - 200, HEIGHT // 2))
    main_display.blit(FONT.render(str(score), True, COLOR_BLUE), (WIDTH - 50, 20))
    main_display.blit(player, player_rect)

    #print(len(enemies))

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.remove(enemy)




