import matplotlib.pyplot as plt
import logging, os
import numpy as np
import argparse

logging.basicConfig(level=getattr(logging, os.getenv('DEBUG', 'INFO')))
logger = logging.getLogger('qlearner')

def plot_linear(xs, ys, fname=None):
    assert (len(xs) == len(ys)), "length mismatch between axises"
    plt.plot(xs, ys, c='b')
    if (fname):
        plt.savefig(fname)
        plt.close()

parser = argparse.ArgumentParser()
parser.add_argument("--show", type=bool, default=False, help="show game progress")
parser.add_argument("--save_resume", type=bool, default=False, help="save and resume?")
parser.add_argument("--start_epsilon", type=float, default=1, help="starting epsilon")
parser.add_argument("--save_freq", type=int, default=100, help="do you want saves? how frequent?")
parser.add_argument("--plot_freq", type=int, default=100, help="do you want plot? how frequent? 0 or -1 to disable")
args = parser.parse_args()

# keeps track of game stats
class GameStats:
  # keeps track of game stats
  def __init__(self, average_length=50, mode='wins'):
    self.mode = mode
    self.wins = 1
    self.losses = 1
    self.draws = 1
    self.illegal_moves = 1 # games w/ changing action space
    # episode specific stats
    self.score = 0
    self.high_score = 0
    self.rewards = 0
    self.scores = LinkedRing(average_length)
    self.history = {
      'scores': [],
      'rewards': [],
      'win_rate': [],
      'draw_rate': [],
      'illegal_moves': []
    }
    self.episodes = 0

  def won(self):
    self.wins += 1

  def lost(self):
    self.losses += 1

  def draw(self):
    self.draws += 1

  def illegal_move(self):
    self.illegal_moves += 1

  # or total episodes
  def total_games(self):
    return float(self.wins + self.losses + self.draws)

  def total_successful_games(self):
    return float(self.wins + self.losses + self.draws)

  def win_rate(self):
    return round(self.wins/self.total_games(), 2)

  def draw_rate(self):
    return round(self.draws/self.total_games(), 2)

  # called after each episode is finished
  def reset_episode(self):
    self.episodes += 1
    self.save_score(self.score)
    # keep history for analysis (plot)
    self.history['scores'].append(self.score)
    self.history['rewards'].append(self.rewards)
    self.history['win_rate'].append(self.win_rate())
    self.history['draw_rate'].append(self.draw_rate())
    # self.history.illegal_moves.append(self.illegal_moves)

    # reset the counters for cur episode
    self.score = 0
    self.rewards = 0


  def add_reward(self, reward):
    self.rewards += reward

  def add_score(self, score):
    self.score += score
    if score > self.high_score:
      self.high_score = score

  def save_score(self, score):
    self.scores.add_val(score)

  def average_score(self):
    return self.scores.average()

  # updates stats based on feedback from the game driver in batch
  def update_stats(self, stats):
    if (stats['won']):
      self.won()
    elif (stats['lost']):
      self.lost()
    elif (stats['draw']):
      self.draw()
    self.add_score(stats['score'])
    self.add_reward(stats['reward'])

  def plot(self, name):
    # TODO average n points together before plotting
    xs = np.linspace(0, self.episodes-1, self.episodes)
    plot_linear(xs, self.history['rewards'], fname=f'figs/{name}-rewards.jpg')
    if (self.mode == 'wins'):
      plot_linear(xs, self.history['win_rate'], fname=f'figs/{name}-win_rate.jpg')
    else:
      plot_linear(xs, self.history['scores'], fname=f'figs/{name}-scores.jpg')

  def __string__(self):
    pass #TODO factor out it from player (maybe..)


class Link(object):
    def __init__(self, value=0.0):
        self.next = None
        self.value = value

class LinkedRing(object):
    def __init__(self, length):
        self.sum = 0.0
        self.length = length
        self.current = Link()

        # Initialize all the nodes:
        last = self.current
        for i in range(length-1):  # one link is already created
            last.next = Link()
            last = last.next
        last.next = self.current  # close the ring

    def add_val(self, val):
        self.sum -= self.current.value
        self.sum += val
        self.current.value = val
        self.current = self.current.next

    def average(self):
        return self.sum / self.length

if __name__ == '__main__':
# Test example:
  rolling_sum = LinkedRing(5)
  while True:
      x = float(input())
      rolling_sum.add_val(x)
      print(">> Average: %f" % rolling_sum.average())
