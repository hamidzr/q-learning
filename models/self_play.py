# how do you learn when you get rewarded just because of the stupidity of the other one

NONE = 0

# setups the episode for
def setup_episode(p):
  state = p.game.state()
  p.last_action = p.agent.act(state)
  p.last_state = state

# one move from one side
def move(p):
  next_state, reward, isDone, info = p.game.feedback(p.role)
  p.agent.remember(p.last_state, p.last_action, reward, next_state, isDone)
  p.last_state = next_state
  action = p.agent.act(next_state) # comeup with an action
  if p.game._game.board[action][0] != NONE:
    action = p.agent.act(next_state) # comeup with an action
  p.last_action = action

  # TODO factor this out to appropriate section
  try:
    p.game.act(action, p.role) # take the action
  except Exception as e:
    isDone = True
    reward = -10
    p.agent.remember(p.last_state, p.last_action, reward, next_state, isDone)

  return isDone

# play untill episode is over
def play(p1, p2):
  # init
  moveNum = 0
  isDone = False
  max_moves = p1.max_moves

  setup_episode(p1)
  move(p1)
  setup_episode(p2)
  move(p2)

  while moveNum < max_moves and not isDone:
    # TODO setup initial state and action for p1 n p2
    isDone = move(p1)

    isDone = move(p2)

    moveNum += 1
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
