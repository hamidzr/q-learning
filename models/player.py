import numpy as np
import os.path
from models.self_play import play
from utils.helpers import GameStats

# or trainee
# game is the standardized game driver
class Player:
  def __init__(self, max_moves=None, name="aiPlayer", agent=None, game=None, role=None, log='wins'):
    self.stats = GameStats(mode=log)
    self.game = game
    self.agent = agent
    self.max_moves = max_moves #max number of moves in a game
    self.name = name
    self.save_loc = f'weights/{name}-player.h5'
    self.last_action = None
    self.last_state = None
    self.role = role

  def run_episode(self, resume, show, opponent):
    self.game.reset()
    if (opponent): # play against another AI
      play(self, opponent)
      self.log()
      opponent.log()
      self.on_episode_done() # has to be called after logging
      opponent.on_episode_done()
    else:
      state = self.game.state()
      for moveNum in range(self.max_moves):
        action = self.agent.act(state)
        if self.role: # or handle it on step?
          next_state, reward, isDone, info = self.game.step(action, self.role)
        else:
          next_state, reward, isDone, info = self.game.step(action)
        self.agent.remember(state, action, reward, next_state, isDone)
        state = next_state
        if show: self.game.show()
        self.stats.update_stats(info)
        if isDone:
          print(f'finished episode w/ {moveNum} moves')
          self.log()
          self.on_episode_done()
          return # breaks out of the loop
      # TODO check this situation
      print('ran out of moves')
      ##### end of episode

  # learns and resets stats
  def on_episode_done(self):
    # reset episode related stat counters
    self.stats.reset_episode()
    self.agent.update_target_model()
    # train the DNN if there are enough memories
    self.agent.attempt_replay()
    # put out logs TODO: based on win/loss or reward

  def log(self):
    system = self.stats.mode
    assert system, 'no logging system defined'
    msg = f"p:{self.name} e: {self.agent.epsilon:.2},"
    if system == 'wins':
      msg += f"win/all: {self.stats.win_rate()} - draws/all {self.stats.draw_rate()}"
    elif system == 'score':
      msg += f" score: {self.stats.score} avg:{self.stats.average_score()}, rewards: {float(self.stats.rewards):.5}"
    print(msg)


  # log types 'wins' and 'score': (regression?!)
  def train(self, episodes=10000, resume=False, plot_freq=None, save_freq=100, show=False, opponent=None):
    if resume and os.path.isfile(self.save_loc):
      print('loading from a previous training')
      self.agent.load(self.save_loc)
    for e in range(episodes):
      print(f'ep: {e}/{episodes} ================ begin ============')
      self.run_episode(resume, show, opponent)
      # save an snapshot every so often
      if plot_freq and plot_freq > 0 and e % plot_freq == 0:
        self.stats.plot(self.name)
      if resume and e % save_freq == 0:
        self.agent.save(self.save_loc)
        if opponent: opponent.agent.save(opponent.save_loc)
