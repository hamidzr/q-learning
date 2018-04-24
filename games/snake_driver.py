from models.game import Game
from utils.helpers import stats_structure
import numpy as np
import math

"""
stat definitions:
  score: number of fruits
  rewards: described in code
"""

DIRS = ['UP', 'RIGHT', 'DOWN', 'LEFT']
DIR_TO_NUM = {
  "UP": 0,
  "RIGHT": 1,
  "DOWN": 2,
  "LEFT": 3,
}


class SnakeDriver(Game):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def todo_state(self):
    """ the state should show:
      1. where the walls and the rest of the snake is.
      2. where the fruits are
    """
    pass

  def naive_state(self):
    # OPTIMIZE or the naive way: show everything as a big matrix
    SNAKE_NUM, FRUIT_NUM = 0.5, 1
    state = np.zeros((self.game.board_size, self.game.board_size))
    for pt in self.game.snake:
      state[pt[0]][pt[1]] = SNAKE_NUM
    fruit = self.game.fruit
    state[fruit[0]][fruit[1]] = FRUIT_NUM

    flat_state = np.array(state).reshape((1,np.power(self.game.board_size, 2)))
    return flat_state

  # single cell snake w/ no growth
  def single_cell_state(self):
    SNAKE_NUM, FRUIT_NUM = [0,1], [1,0]
    # state = [position of fruit, position of snake cell, direction]
    one_hot_direction = np.zeros(4)
    one_hot_direction[DIR_TO_NUM[self.game.direction]] = 1
    # normalize positions
    positions = np.concatenate((self.game.fruit, self.game.snake[0])) / self.game.board_size
    state = np.concatenate((positions, one_hot_direction))
    state = state.reshape(1, state.shape[0])
    return state

  # TODO add walls to the state, onehot encode?
  def state(self):
    # return self.naive_state()
    return self.single_cell_state()

  def step(self, action):
    # 0: left, 1: right, 2: keep going straight
    ACTION_STR = ['TURN_LEFT', 'TURN_RIGHT', 'KEEP_GOING']
    # print( 'cur dir', self.game.direction, ACTION_STR[action]) # check the actions taken

    isAlive, gotFruit = self.game.step_relative(ACTION_STR[action])

    dis_to_fruit = distance(self.game.snake[0], self.game.fruit)

    # reward = -1 * dis_to_fruit / self.game.board_size
    reward = -0.1
    stats = stats_structure()
    if not isAlive:
      reward -= 20
    if gotFruit:
      stats['score'] = 1
      reward += 10
    reward = float(reward)

    new_state = self.state()
    isDone = not isAlive
    stats['reward'] = reward

    return new_state, reward, isDone, stats

  def show(self):
    self.game.print_field()

  def reset(self):
    self.game.reset()

def distance(pt1, pt2):
  return math.sqrt(math.pow(pt1[0]-pt2[0], 2) + math.pow(pt1[1]-pt2[1], 2))
