from models.game import Game
from utils.helpers import stats_structure, one_hot
import numpy as np

class TicTacToe(Game):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def state(self):
    state = self.game.squares[:] # make a copy
    # map x and o to numbers
    # TODO provide reverse mapper
    for idx, val in enumerate(state):
      if val == 'O':
        state[idx] = 1
      if val == 'X':
        state[idx] = 2
      if val == None:
        state[idx] = 0
    state = np.array(state)
    # state = state.reshape(1, len(state))
    state = one_hot(state, 2) # onehot encode
    one_d = np.concatenate(state)
    one_d = one_d.reshape(1, len(one_d))
    return one_d

  def step(self, action, role):
    # compute the state into NN friendly format, normalize etc
    reward = 0
    stats = stats_structure()
    if not action in self.game.available_moves():
      new_state = self.state()
      reward = -15
      isDone = True
      stats['reward'] = reward
      return new_state, reward, isDone, stats
    # prepare the new_state
    self.game.move_and_respond(action, role)
    new_state = self.state()

    # is it finished?
    isDone = self.game.complete() # OPTIMIZE recomputing the winner

    # define the rewards
    info = self.game.winner()
    if isDone:
      if info ==  role:
        stats['won'] = True
        reward = 10
      elif info == self.game.get_enemy(role):
        stats['lost'] = True
        reward = -10
      else: # draw
        assert info == None, 'bad game winner'
        stats['draw'] = True
        reward = 0
    else: # reward for picking a valid action..
      reward = 1
    reward = float(reward)

    stats['reward'] = reward
    return new_state, reward, isDone, stats

  def show(self):
    self.game.show()

  def reset(self):
    self.game.reset()
