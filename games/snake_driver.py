from models.game import Game
from utils.helpers import GameStats
import numpy as np

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
    SNAKE_NUM, FRUIT_NUM = 0.5, -1
    state = np.zeros((self._game.board_size, self._game.board_size))
    for pt in self._game.snake:
      state[pt[0]][pt[1]] = SNAKE_NUM
    fruit = self._game.fruit
    state[fruit[0]][fruit[1]] = FRUIT_NUM

    return state

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

    reward = 0.1
    if not isAlive:
      reward -= 50
    if gotFruit:
      self.stats.add_score(1)
      reward += 5

    self.stats.add_reward(reward)

    new_state = self.state()
    isDone = not isAlive

    return new_state, reward, isDone, None

  def show(self):
    self._game.print_field()

  def reset(self):
    self._game.reset()
