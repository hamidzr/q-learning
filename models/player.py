import numpy as np
import os.path

# or trainee
# game is the standardized game driver
class Player:
  def __init__(self, max_moves=None, name="aiPlayer", agent=None, game=None):
    self.game = game
    self.agent = agent
    self.max_moves = max_moves #max number of moves in a game
    self.name = name
    self.save_loc = f'weights/{name}-player.h5'

  # log types 'wins' and 'score': (regression?!)
  def train(self, episodes=10000, resume=False, save_freq=100, show=False, log='wins'):
    if resume and os.path.isfile(self.save_loc):
      self.agent.load(self.save_loc)
    for e in range(episodes):
      self.game.reset()
      state = self.game.state()
      for moveNum in range(self.max_moves):
        action = self.agent.act(state)
        # TODO factor out role 'X'
        next_state, reward, isDone, info = self.game.step(action)
        self.agent.remember(state, action, reward, next_state, isDone)
        state = next_state
        if isDone: # when episode finished
          # update game stats
          self.agent.update_target_model()
          # put out logs TODO: based on win/loss or score
          msg = f"ep: {e}/{episodes}, moves: {moveNum}, e: {self.agent.epsilon:.2},"
          if log == 'wins':
            msg += f"win/all: {self.game.stats.win_rate()} - draws/all {self.game.stats.draw_rate()}"
          elif log == 'score':
            msg += f" score: {self.game.stats.score} avg:{self.game.stats.average_score()}, rewards: {float(self.game.stats.rewards):.5}"
          print(msg)

          if show: self.game.show()
          # reset episode related stat counters
          self.game.stats.reset_episode()
          break
        # end of episode
      # train the DNN if there are enough memories
      self.agent.attempt_replay()
      # save an snapshot every so often
      if resume and e % save_freq == 0:
        self.agent.save(self.save_loc)
