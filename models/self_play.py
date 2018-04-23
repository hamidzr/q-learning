# how do you learn when you get rewarded just because of the stupidity of the other one

NONE = 0

class TwoPOrchestrator:
  def __init__(self, p1, p2):
    self.p1 = p1
    self.p2 = p2

  # setups the episode for
  def setup_episode(self, p):
    state = p.game.state()
    p.last_action = p.agent.act(state)
    p.last_state = state

  # one move from one side
  def move(self, p):
    next_state, reward, isDone, info = p.game.feedback(p.role)
    p.stats.update_stats(info)
    p.agent.remember(p.last_state, p.last_action, reward, next_state, isDone)
    p.last_state = next_state
    action = p.agent.act(next_state) # comeup with an action
    if p.game.game.board[action][0] != NONE:
      action = p.agent.act(next_state) # comeup with an action
    p.last_action = action

    # TODO factor this out to appropriate section
    try:
      p.game.act(action, p.role) # take the action
    except Exception as e:
      print('violating action no1 won')
      isDone = True
      reward = -10
      p.agent.remember(p.last_state, p.last_action, reward, next_state, isDone)

    return isDone

  # play untill episode is over
  def play(self):
    # init
    moveNum = 0
    isDone = False
    max_moves = self.p1.max_moves

    self.setup_episode(self.p1)
    self.move(self.p1)
    self.setup_episode(self.p2)
    self.move(self.p2)

    while moveNum < max_moves and not isDone:
      # TODO setup initial state and action for self.p1 n self.p2
      isDone = self.move(self.p1)
      if (isDone):
        next_state, reward, isDone, info = self.p2.game.feedback(self.p2.role)
        self.p2.stats.update_stats(info)
        break

      isDone = self.move(self.p2)
      if (isDone):
        next_state, reward, isDone, info = self.p1.game.feedback(self.p1.role)
        self.p1.stats.update_stats(info)
        break

      moveNum += 1

  def get_enemy(self, p):
    if (p == self.p1):
      return self.p2
    else:
      return self.p1

def play(p1, p2):
  orch = TwoPOrchestrator(p1, p2)
  orch.play()
#   max_moves = p1.max_moves
#   isDone = False
#   # p1 act get isDone
#   action = p1.agent.act(state)
#   print('p1 act')
#   while not isDone and max_moves:
#     # if isDone at any step both do a step and finish episode
#     # a: p2 act get isDone
#     print('p2 act')
#     # p1 do step get isDone
#     print('p1 step')
#     # p1 act get isDone
#     print('p1 act')
#     print('p2 step')
#     # p2 do step getisDone
#     # go to a:
#   print('p1 step')
#   print('p2 step')
