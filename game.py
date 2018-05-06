import pygame
import math
import random
from pygame.locals import *
import time
pygame.init()
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))

cellSize = width / 50
gridHeight = height / cellSize
gridWidth = width / cellSize

white = (255, 255, 255)
red = (255, 0, 0)

keys = [False, False, False, True]
snakeGridPos = [(math.floor(gridWidth/2), math.floor(gridHeight/2))]
foodGridPos = (random.randint(0, gridWidth-1), random.randint(0, gridHeight-1))
ateFood = False
score = 0
pygame.display.set_caption("Score: " + str(score))

print(gridWidth, gridHeight)

while True:
    screen.fill(0)
    for snakeTile in snakeGridPos:
        tileCoords = (snakeTile[0]*cellSize, snakeTile[1]*cellSize)
        pygame.draw.rect(screen, white, (tileCoords[0], tileCoords[1], cellSize, cellSize), 0)

    foodCoords = (foodGridPos[0]*cellSize, foodGridPos[1]*cellSize)
    pygame.draw.rect(screen, red, (foodCoords[0], foodCoords[1], cellSize, cellSize), 0)

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            keys = [False, False, False, False]
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True

    snakeGridPos.insert(0, snakeGridPos[len(snakeGridPos) - 1])
    if keys[0]:
        snakeGridPos[0] = (snakeGridPos[1][0], snakeGridPos[1][1] - 1)
    if keys[1]:
        snakeGridPos[0] = (snakeGridPos[1][0] - 1, snakeGridPos[1][1])
    if keys[2]:
        snakeGridPos[0] = (snakeGridPos[1][0], snakeGridPos[1][1] + 1)
    if keys[3]:
        snakeGridPos[0] = (snakeGridPos[1][0] + 1, snakeGridPos[1][1])

    if snakeGridPos[0][0] < 0: break
    elif snakeGridPos[0][0] >= gridWidth: break
    elif snakeGridPos[0][1] < 0: break
    elif snakeGridPos[0][1] >= gridHeight: break

    if snakeGridPos.count(snakeGridPos[0]) > 1: break

    if snakeGridPos[0] == foodGridPos:
        ateFood = True
        score = score + 1
        pygame.display.set_caption("Score: " + str(score))
        foodGridPos = (random.randint(0, gridWidth-1), random.randint(0, gridHeight-1))

    if not ateFood:
        snakeGridPos.pop(len(snakeGridPos)-1)

    ateFood = False
    print(score)

    time.sleep(0.1)

time.sleep(5)
pygame.quit()
exit(0)