from models.game import Game
import numpy as np

# how do you learn when you get rewarded just because of the stupidity of the other one
class Driver(Game):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def state(self):
    state = np.array(self.game.board).flatten()
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
    new_state = self.state()
    winner = self.game.getWinner()
    if winner:
      print('winner', winner)
      isDone = True
      if winner == role:
        self.stats.won()
        reward += 10
      else: # role lost
        reward += -10
        self.stats.lost()
    return new_state, reward, isDone, None

  def show(self):
    self.printBoard()

  def reset(self):
    pass

if __name__ == '__main__':
  from games.connectn import Game
  baseGame = Game()
  game = Driver(base_game=baseGame)
  game.test()
