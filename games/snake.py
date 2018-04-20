import pygame
from pygame.locals import *
from random import randint
import os, sys, time

DIRECTIONS = {
  "LEFT": (-1, 0),
  "RIGHT": (1, 0),
  "UP": (0, 1),
  "DOWN": (0, -1),
}

class SnakeG:
  def __init__(self, board_size=50, grow=True,
               random_start=False, initial_snake=None):
    self.snake = [(0, 2), (0, 1), (0, 0)]
    if initial_snake != None: self.snake = initial_snake
    self.fruit = None
    self.board_size = board_size
    if random_start:
      self.place_fruit()
    else:
      self.place_fruit((self.board_size // 2, self.board_size // 2))
    self.direction = 'UP' # WARN assuming it starts upwards always
    self.grow = grow
    self.random_start = random_start
    self.initial_snake = initial_snake

  def reset(self):
    self.__init__(board_size=self.board_size, grow=self.grow, random_start=self.random_start, initial_snake=self.initial_snake)

  def place_fruit(self, coord=None):
    if coord:
      self.fruit = coord
      return

    while True:
      x = randint(0, self.board_size-1)
      y = randint(0, self.board_size-1)
      if (x, y) not in self.snake:
         self.fruit = x, y
         return

  # returns (isAlive, gotFruit)
  def step(self, direction):
    self.direction = direction
    old_head = self.snake[0]
    movement = DIRECTIONS[direction]
    new_head = (old_head[0]+movement[0], old_head[1]+movement[1])
    got_fruit = False

    if (
        new_head[0] < 0 or
        new_head[0] >= self.board_size or
        new_head[1] < 0 or
        new_head[1] >= self.board_size or
        new_head in self.snake
      ):
      return False, got_fruit # game over

    if new_head == self.fruit:
      got_fruit = True
      self.place_fruit()
      if not self.grow:
        tail = self.snake[-1]
        del self.snake[-1]
    else:
      tail = self.snake[-1]
      del self.snake[-1]

    self.snake.insert(0, new_head)
    return True, got_fruit

  def print_field(self):
    os.system('clear')
    print('=' * (self.board_size+2))
    for y in range(self.board_size-1, -1, -1):
      print('|', end='')
      for x in range(self.board_size):
        out = ' '
        if (x, y) in self.snake:
          out = 'X'
        elif (x, y) == self.fruit:
          out = 'O'
        print(out, end='')
      print('|')
    print('=' * (self.board_size+2))

def test():
  snakeGame = SnakeG()
  assert snakeGame.step('UP')[0]

  assert snakeGame.snake == [(0, 3), (0, 2), (0, 1)]

  snakeGame.fruit = (0, 4)
  assert snakeGame.step('UP')[0]

  assert snakeGame.snake == [(0, 4), (0, 3), (0, 2), (0, 1)]
  assert snakeGame.fruit != (0, 4)

  assert not snakeGame.step('DOWN')[0], 'error from test'

def run():
  DIRS = ['UP', 'RIGHT', 'DOWN', 'LEFT']
  game = SnakeG()

  direction = 0

  pygame.init()
  s = pygame.display.set_mode((game.board_size * 10, game.board_size * 10))
  #pygame.display.set_caption('Snake')
  appleimage = pygame.Surface((10, 10))
  appleimage.fill((0, 255, 0))
  img = pygame.Surface((10, 10))
  img.fill((255, 0, 0))
  clock = pygame.time.Clock()

  pygame.time.set_timer(1, 100)

  while True:
    events = pygame.event.get()
    for e in events:
      if e.type == pygame.KEYDOWN:
        if e.key == pygame.K_LEFT:
          direction = (direction+3) % 4
        if e.key == pygame.K_RIGHT:
          direction = (direction+1) % 4
    time.sleep(100/1000.0)

    if not game.step(DIRS[direction]):
      pygame.quit()
      sys.exit(1)

    s.fill((255, 255, 255))
    for bit in game.snake:
      s.blit(img, (bit[0] * 10, (game.board_size - bit[1] - 1) * 10))
    s.blit(appleimage, (game.fruit[0] * 10, (game.board_size - game.fruit[1]-1) * 10))
    pygame.display.flip()

if __name__ == '__main__':
  test()
  run()
