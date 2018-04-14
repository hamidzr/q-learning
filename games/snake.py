import pygame
from pygame.locals import *
from random import randint
import os, sys

ARRAY_SIZE = 50

DIRECTIONS = {
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
    "UP": (0, 1),
    "DOWN": (0, -1),
}

snake, fruit = None, None

def init():
    global snake
    snake = [ (0, 2), (0, 1), (0, 0)]

    place_fruit((ARRAY_SIZE // 2, ARRAY_SIZE // 2))

def place_fruit(coord=None):
    global fruit
    if coord:
        fruit = coord
        return

    while True:
        x = randint(0, ARRAY_SIZE-1)
        y = randint(0, ARRAY_SIZE-1)
        if (x, y) not in snake:
           fruit = x, y
           return

def step(direction):
    old_head = snake[0]
    movement = DIRECTIONS[direction]
    new_head = (old_head[0]+movement[0], old_head[1]+movement[1])

    if (
            new_head[0] < 0 or
            new_head[0] >= ARRAY_SIZE or
            new_head[1] < 0 or
            new_head[1] >= ARRAY_SIZE or
            new_head in snake
        ):
        return False
        
    if new_head == fruit:
        place_fruit()
    else:
        tail = snake[-1]
        del snake[-1]

    snake.insert(0, new_head)
    return True

def print_field():
    os.system('clear')
    print('=' * (ARRAY_SIZE+2))
    for y in range(ARRAY_SIZE-1, -1, -1):
        print('|', end='')
        for x in range(ARRAY_SIZE):
            out = ' '
            if (x, y) in snake:
                out = 'X'
            elif (x, y) == fruit:
                out = 'O'
            print(out, end='')
        print('|')
    print('=' * (ARRAY_SIZE+2))

def test():
    global fruit
    init()
    assert step('UP')

    assert snake == [(0, 3), (0, 2), (0, 1)]

    fruit = (0, 4)
    assert step('UP')

    assert snake == [(0, 4), (0, 3), (0, 2), (0, 1)]
    assert fruit != (0, 4)

    assert not step('DOWN'), 'Kdyz nacouvam do sebe, umru!'

DIRS = ['UP', 'RIGHT', 'DOWN', 'LEFT']
def run():
    init()

    direction = 0

    pygame.init()
    s = pygame.display.set_mode((ARRAY_SIZE * 10, ARRAY_SIZE * 10))
    #pygame.display.set_caption('Snake')
    appleimage = pygame.Surface((10, 10))
    appleimage.fill((0, 255, 0))
    img = pygame.Surface((10, 10))
    img.fill((255, 0, 0))
    clock = pygame.time.Clock()

    pygame.time.set_timer(1, 100)

    while True:
        e = pygame.event.wait()
        if e.type == QUIT:
            pygame.quit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 3:
                direction = (direction+1) % 4
            elif e.button == 1:
                direction = (direction+3) % 4

        if not step(DIRS[direction]):
            pygame.quit()
            sys.exit(1)

        s.fill((255, 255, 255))	
        for bit in snake:
            s.blit(img, (bit[0] * 10, (ARRAY_SIZE - bit[1] - 1) * 10))
        s.blit(appleimage, (fruit[0] * 10, (ARRAY_SIZE - fruit[1]-1) * 10))
        pygame.display.flip()
run()
