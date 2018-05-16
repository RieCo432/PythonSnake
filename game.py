import pygame
import math
import random
from pygame.locals import *
import time
from datetime import datetime
import os

window_x, window_y = 5, 32
width, height = 1320, 680

cellSize = 20

moves_per_second = 10

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (window_x, window_y)
pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill(0)

gridHeight = height / cellSize
gridWidth = width / cellSize

white = (255, 255, 255)
red = (255, 0, 0)
yellow = (128, 255, 0)
black = (0, 0, 0)

move_timedelta = 1000000.0 / moves_per_second # in microseconds


def start_game():

    keys = [False, False, False, False]
    snake_grid_pos = [(math.floor((gridWidth-1)/2), math.floor((gridHeight-1)/2))]
    food_grid_pos = (random.randint(0, gridWidth-1), random.randint(0, gridHeight-1))
    ate_food = False
    score = 0
    pygame.display.set_caption("Score: " + str(score))

    game_over = False

    last_frame_timestamp = datetime.now()

    pygame.draw.rect(screen, yellow,
                     (snake_grid_pos[0][0] * cellSize, snake_grid_pos[0][1] * cellSize, cellSize, cellSize), 0)
    pygame.display.flip()

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                keys = [False, False, False, False]
                if event.key == K_UP:
                    keys[0] = True
                elif event.key == K_LEFT:
                    keys[1] = True
                elif event.key == K_DOWN:
                    keys[2] = True
                elif event.key == K_RIGHT:
                    keys[3] = True

        if (datetime.now() - last_frame_timestamp).microseconds > move_timedelta:

            snake_grid_pos.insert(0, snake_grid_pos[len(snake_grid_pos) - 1])
            if keys[0]:
                snake_grid_pos[0] = (snake_grid_pos[1][0], snake_grid_pos[1][1] - 1)
            if keys[1]:
                snake_grid_pos[0] = (snake_grid_pos[1][0] - 1, snake_grid_pos[1][1])
            if keys[2]:
                snake_grid_pos[0] = (snake_grid_pos[1][0], snake_grid_pos[1][1] + 1)
            if keys[3]:
                snake_grid_pos[0] = (snake_grid_pos[1][0] + 1, snake_grid_pos[1][1])

            if snake_grid_pos[0][0] < 0:
                game_over = True
            elif snake_grid_pos[0][0] >= gridWidth:
                game_over = True
            elif snake_grid_pos[0][1] < 0:
                game_over = True
            elif snake_grid_pos[0][1] >= gridHeight:
                game_over = True

            if (snake_grid_pos.count(snake_grid_pos[0]) > 1) and (len(snake_grid_pos) > 2):
                game_over = True

            if snake_grid_pos[0] == food_grid_pos:
                ate_food = True
                score = score + 1
                pygame.display.set_caption("Score: " + str(score))
                food_grid_pos = (random.randint(0, gridWidth-1), random.randint(0, gridHeight-1))

            if not ate_food:
                snake_ghost_pos = snake_grid_pos[-1]
                snake_grid_pos.pop(len(snake_grid_pos)-1)
            ate_food = False

            pygame.draw.rect(screen, yellow,
                             (snake_grid_pos[0][0] * cellSize, snake_grid_pos[0][1] * cellSize, cellSize, cellSize), 0)
            if len(snake_grid_pos) >= 2:
                pygame.draw.rect(screen, white,
                             (snake_grid_pos[1][0] * cellSize, snake_grid_pos[1][1] * cellSize, cellSize, cellSize), 0)
            if keys[0] or keys[1] or keys[2] or keys[3]:
                pygame.draw.rect(screen, black,
                             (snake_ghost_pos[0] * cellSize, snake_ghost_pos[1] * cellSize, cellSize, cellSize),
                             0)

            pygame.draw.rect(screen, red, (food_grid_pos[0] * cellSize, food_grid_pos[1] * cellSize, cellSize, cellSize), 0)

            pygame.display.flip()
            last_frame_timestamp = datetime.now()

    show_score(score)


def show_score(score):

    pygame.font.init()
    my_font = pygame.font.SysFont("Comic Sans MS", 60)

    text_surface = my_font.render("Score: " + str(score), True, red)
    text_rect = text_surface.get_rect()
    text_rect.center = (width / 2, height / 2)
    screen.blit(text_surface, text_rect)

    my_font = pygame.font.SysFont("Comic Sans MS", 20)
    instruct_text = my_font.render("Press any key to restart game", True, white)
    text_rect = instruct_text.get_rect()
    text_rect.center = (width / 2, height - 20)
    screen.blit(instruct_text, text_rect)

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                time.sleep(2)
                screen.fill(0)
                start_game()
        time.sleep(0.001)

start_game()

pygame.quit()
exit(0)
