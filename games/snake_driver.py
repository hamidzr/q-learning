from models.game import Game
from utils.helpers import GameStats
import numpy as np

class TicTacToe(Game):
  def __init__(self, base_game=None):
    self._game = base_game
    self.stats = GameStats()

  def state(self):
    """ the state should show:
      1. where the walls and the rest of the snake is.
      2. where the fruits are
    """
    # or the naive way: show everything as a big matrix
    SNAKE_NUM, FRUIT_NUM = 0.5, -1
    state = np.zeros((self._game.board_size, self._game.board_size))
    for pt in self._game.snake:
      state[pt[0]][pt[1]] = SNAKE_NUM
    for pt in self._game.fruit:
      state[pt[0]][pt[1]] = FRUIT_NUM

    return state

  def step(self, action):
    pass

  def show(self):
    pass

  def reset(self):
    pass
