# how do you learn when you get rewarded just because of the stupidity of the other one

NONE = 0

class TwoPOrchestrator:
  def __init__(self, pA, pB):
    self.pA = pA
    self.pB = pB
    self.starter = pA

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
      isDone = True
      reward = -10
      p.stats.add_reward(reward)
      p.stats.lost()
      p.agent.remember(p.last_state, p.last_action, reward, next_state, isDone)
      # enemy wins
      self.get_opponent(p).stats.won()
    return isDone

  # play untill episode is over
  # TODO swap who goes first at every game
  def play(self):
    # init
    firstP = self.starter;
    secondP = self.get_opponent(self.starter);
    moveNum = 0
    isDone = False
    max_moves = firstP.max_moves

    self.setup_episode(firstP)
    self.move(firstP)
    self.setup_episode(secondP)
    self.move(secondP)

    while moveNum < max_moves and not isDone:
      # TODO setup initial state and action for firstP n secondP
      isDone = self.move(firstP)
      if (isDone):
        next_state, reward, isDone, info = secondP.game.feedback(secondP.role)
        secondP.stats.update_stats(info)
        break

      isDone = self.move(secondP)
      if (isDone):
        next_state, reward, isDone, info = firstP.game.feedback(firstP.role)
        firstP.stats.update_stats(info)
        break

      moveNum += 1

    # swap play order for the next game
    self.starter = self.get_opponent(self.starter)

  def get_opponent(self, p):
    if (p == self.pA):
      return self.pB
    else:
      return self.pA

# keeping the api unchanged
def play(pA, pB):
  orch = TwoPOrchestrator(pA, pB)
  orch.play()
#   max_moves = pA.max_moves
#   isDone = False
#   # pA act get isDone
#   action = pA.agent.act(state)
#   print('pA act')
#   while not isDone and max_moves:
#     # if isDone at any step both do a step and finish episode
#     # a: pB act get isDone
#     print('pB act')
#     # pA do step get isDone
#     print('pA step')
#     # pA act get isDone
#     print('pA act')
#     print('pB step')
#     # pB do step getisDone
#     # go to a:
#   print('pA step')
#   print('pB step')
