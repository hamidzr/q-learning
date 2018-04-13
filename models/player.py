import numpy as np

# or trainee
# game is the standardized game driver
class Player:
  def __init__(self, max_moves=None, name="aiPlayer", agent=None, game=None):
    self.game = game
    self.agent = agent
    self.max_moves = max_moves #max number of moves in a game
    self.name = name
    self.save_loc = f'{name}-player.h5'

  def train(self, episodes=10000, resume=False, show=False):
    if resume: self.agent.load(self.save_loc)
    for e in range(episodes):
      self.game.reset()
      state = self.game.state()
      for moveNum in range(self.max_moves):
        action = self.agent.act(state)
        # TODO factor out role 'X'
        next_state, reward, isDone, info = self.game.step(action, 'X')
        self.agent.remember(state, action, reward, next_state, isDone)
        state = next_state
        if isDone: # when episode finished
          # update game stats
          self.agent.update_target_model()
          # put out logs
          print(f"ep: {e}/{episodes}, moves: {moveNum}, e: {self.agent.epsilon:.2}, win/all: {self.game.stats.win_rate()} - draws/all {self.game.stats.draw_rate()}")
          if show: self.game.show()
          break
        # end of episode
      # train the DNN if there are enough memories
      self.agent.attempt_replay()
      # save an snapshot every so often
      if resume and e % 100 == 0:
        self.agent.save(SAVE_LOC)
