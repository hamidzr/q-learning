from models.game import Game
import numpy as np

class TicTacToe(Game):
  def __init__(self, base_game=None):
    self._game = base_game

  def state(self):
    state = self._game.squares[:] # make a copy
    # map x and o to numbers
    # TODO provide reverse mapper
    for idx, val in enumerate(state):
      if val == 'O':
        state[idx] = 1
      if val == 'X':
        state[idx] = -1
      if val == None:
        state[idx] = 0
    state = np.array(state).reshape(1, len(state))
    # TODO normalize state
    return state

  def step(self, action, player):
    # compute the state into NN friendly format, normalize etc
    print('making a move', action, player)
    if not action in self._game.available_moves():
      print(f'{action} not available in {self._game.available_moves()}')
      new_state = self.state()
      reward = -15
      isDone = True
      return new_state, reward, isDone, self._game.WRONG_MOVE
    # prepare the new_state
    self._game.move_and_respond(action, player)
    new_state = self.state()
    # define the rewards
    info = self._game.winner()
    if info ==  player:
      reward = 10
    elif info == self._game.get_enemy(player):
      reward = -10
    else: # reward for picking a valid action..
      reward = 2
    reward = float(reward)

    # is it finished?
    isDone = self._game.complete() # OPTIMIZE recomputing the winner
    return new_state, reward, isDone, info

  def show(self):
    self._game.show()

  def reset(self):
    self._game.reset()

