from models.game import Game
from utils.helpers import GameStats
import numpy as np
import math

"""
stat definitions:
  score: number of fruits
  rewards: described in code
"""

class SnakeDriver(Game):
  def __init__(self, base_game=None):
    self._game = base_game
    self.stats = GameStats()
    self.cur_direction = 0

  def state(self):
    """ the state should show:
      1. where the walls and the rest of the snake is.
      2. where the fruits are
    """
    # OPTIMIZE or the naive way: show everything as a big matrix
    SNAKE_NUM, FRUIT_NUM = 0.5, 1
    state = np.zeros((self._game.board_size, self._game.board_size))
    for pt in self._game.snake:
      state[pt[0]][pt[1]] = SNAKE_NUM
    fruit = self._game.fruit
    state[fruit[0]][fruit[1]] = FRUIT_NUM

    flat_state = np.array(state).reshape((1,np.power(self._game.board_size, 2)))
    return flat_state

  def step(self, action):
    # 0: left 1: right
    DIRS = ['UP', 'RIGHT', 'DOWN', 'LEFT']
    direction = self.cur_direction
    if action == 0:
      direction = (direction+3) % 4
    elif action == 1:
      direction = (direction+1) % 4
    else:
      assert action == 2, f'bad action {action}'

    isAlive, gotFruit = self._game.step(DIRS[direction])
    self.cur_direction = direction

    dis_to_fruit = distance(self._game.snake[0], self._game.fruit)

    # reward = -1 * dis_to_fruit / self._game.board_size
    reward = 0
    if not isAlive:
      reward -= 20
    if gotFruit:
      self.stats.add_score(1)
      reward += 10
    reward = float(reward)

    self.stats.add_reward(reward)

    new_state = self.state()
    isDone = not isAlive

    return new_state, reward, isDone, None

  def show(self):
    self._game.print_field()

  def reset(self):
    self._game.reset()

def distance(pt1, pt2):
  return math.sqrt(math.pow(pt1[0]-pt2[0], 2) + math.pow(pt1[1]-pt2[1], 2))
