from models.game import Game
from utils.helpers import stats_structure
import numpy as np
import math

class GameDriver(Game):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.cur_state = self.state(self.game.reset())

  def state(self, gym_state=None):
    # gym env has no way to get the state without making an action..
    if (gym_state == None): return self.cur_state
    return np.reshape(gym_state, [1, self.game.observation_space.shape[0]])

  def step(self, action):
    next_state, reward, isDone, _ = self.game.step(action)

    self.cur_state = self.state(next_state)

    stats = stats_structure()
    if isDone:
      reward -= 10
    else:
      stats['score'] = 1
    reward = float(reward)

    new_state = self.state()
    stats['reward'] = reward

    return new_state, reward, isDone, stats

  def show(self):
    self.game.print_field()

  def reset(self):
    self.game.reset()

def distance(pt1, pt2):
  return math.sqrt(math.pow(pt1[0]-pt2[0], 2) + math.pow(pt1[1]-pt2[1], 2))
