from models.game import Game
from utils.helpers import stats_structure
import numpy as np

# how do you learn when you get rewarded just because of the stupidity of the other one
class Driver(Game):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def state(self):
    state = np.array(self.game.board).flatten()
    # TODO each player's state should be repr as one hot encoded
    state = state.reshape(1, len(state))
    return state

  def act(self, action, role):
    # number of actions: self.game.cols
    isDone = False
    self.game.insert(action, role)
    winner = self.game.getWinner()
    if winner: isDone = True
    return isDone

  # if after taking action and waiting for the other game is not over step
  def step(self, action):
    isDone = self.act(action)
    # if not done: wait for other side
    return feedback()

  def feedback(self, role):
    isDone = False
    reward = 0
    stats = stats_structure()
    new_state = self.state()
    winner = self.game.getWinner()
    if winner:
      print('winner', winner)
      self.show()
      isDone = True
      print('win role', winner, role)
      if winner == role:
        stats['won'] = True
        reward += 10
      else: # role lost
        reward += -10
        stats['lost'] = True

    stats['reward'] = reward
    return new_state, reward, isDone, stats

  def show(self):
    self.game.printBoard()

  def reset(self):
    self.game.__init__(cols=self.game.cols, rows=self.game.rows)

if __name__ == '__main__':
  from games.connectn import Game
  baseGame = Game()
  game = Driver(base_game=baseGame)
  game.test()
