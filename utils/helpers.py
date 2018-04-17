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
    self.scores = LinkedRing(50)

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
    self.save_score(self.score)
    self.score = 0
    self.rewards = 0

  def add_reward(self, reward):
    self.rewards += reward

  def add_score(self, score):
    self.score += score
    if score > self.high_score:
      print('record broken!')
      self.high_score = score

  def save_score(self, score):
    print('save dscore', score)
    self.scores.add_val(score)

  def average_score(self):
    return self.scores.average()

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
