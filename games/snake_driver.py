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
  def __init__(self, base_game=None, log='wins'):
    self._game = base_game
    self.stats = GameStats(mode=log)
    self.cur_direction = 0


  def todo_state(self):
    """ the state should show:
      1. where the walls and the rest of the snake is.
      2. where the fruits are
    """
    pass

  def naive_state(self):
    # OPTIMIZE or the naive way: show everything as a big matrix
    SNAKE_NUM, FRUIT_NUM = 0.5, 1
    state = np.zeros((self._game.board_size, self._game.board_size))
    for pt in self._game.snake:
      state[pt[0]][pt[1]] = SNAKE_NUM
    fruit = self._game.fruit
    state[fruit[0]][fruit[1]] = FRUIT_NUM

    flat_state = np.array(state).reshape((1,np.power(self._game.board_size, 2)))
    return flat_state

  # single cell snake w/ no growth
  def single_cell_state(self):
    SNAKE_NUM, FRUIT_NUM = [0,1], [1,0]
    DIR_TO_NUM = {
      "LEFT": 0,
      "RIGHT": 1,
      "UP": 2,
      "DOWN": 3
    }
    # state = [[position of fruit], [position of snake cell], [direction]]
    one_hot_direction = np.zeros(4)
    one_hot_direction[DIR_TO_NUM[self._game.direction]] = 1
    positions = np.concatenate((self._game.fruit, self._game.snake[0])) / self._game.board_size
    state = np.concatenate((positions, one_hot_direction))
    state = state.reshape(1, state.shape[0])
    return state

  def state(self):
    # return self.naive_state()
    return self.single_cell_state()

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
    reward = -0.1
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
