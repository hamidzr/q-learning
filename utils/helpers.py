# keeps track of game stats
class GameStats:
  # keeps track of game stats
  def __init__(self):
    self.wins = 1
    self.losses = 1
    self.draws = 1
    self.illegal_moves = 1 # games w/ changing action space
    # episode specific stats
    self.score = 0
    self.high_score = 0
    self.rewards = 0

  def won(self):
    self.wins += 1

  def lost(self):
    self.losses += 1

  def draw(self):
    self.draws += 1

  def illegal_move(self):
    self.illegal_moves += 1

  def total_games(self):
    return float(self.wins + self.losses + self.draws)

  def win_rate(self):
    return round(self.wins/self.total_games(), 2)

  def draw_rate(self):
    return round(self.draws/self.total_games(), 2)

  def reset_episode(self):
    self.score = 0
    self.rewards = 0

  def add_reward(self, reward):
    self.rewards += reward

  def add_score(self, score):
    self.score += score
    if score > self.high_score:
      print('record broken!')
      self.high_score = score
