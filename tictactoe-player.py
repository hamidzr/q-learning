import numpy as np
from models.dqn import DQNAgent
from games.tictactoe import *
from utils.helpers import GameStats

EPISODES = 20000
MAX_MOVES = 100 # maximum number of moves in a game
SAVE_LOC = "weights/tictactoe-ddqn.h5"

# create the game
board = Tic(random_ratio=0.1)

# setup the agent
state_size = 9
action_size = state_size
batch_size = 32
agent = DQNAgent(state_size, action_size, epsilon=0.05, epsilon_decay=0.995, epsilon_min=0.01)
agent.load(SAVE_LOC)


# game stats
stats = GameStats()
done = False


def prepare_state(game_state):
  state = game_state[:] # make a copy
  # map x and o to numbers
  # TODO provide reverse mapper
  for idx, val in enumerate(state):
    if val == 'O':
      state[idx] = 1
    if val == 'X':
      state[idx] = -1
    if val == None:
      state[idx] = 0
  state = np.array(state).reshape(1, len(state))
  # TODO normalize state
  return state

def step(game, action, player='X'):
  # compute the state into NN friendly format, normalize etc
  if not action in game.available_moves():
    new_state = prepare_state(game.squares)
    reward = -15
    isDone = True
    return new_state, reward, isDone, WRONG_MOVE
  # prepare the new_state
  game.move_and_respond(action, player=player)
  new_state = prepare_state(game.squares)
  # define the rewards
  info = game.winner()
  if info ==  player:
    reward = 10
  elif info == get_enemy(player):
    reward = -10
  else: # reward for picking a valid action..
    reward = 2
  reward = float(reward)

  # is it finished?
  isDone = game.complete() # OPTIMIZE recomputing the winner
  return new_state, reward, isDone, info


player = 'X'
enemy = get_enemy(player)


# TODO more exploration?
for e in range(EPISODES):
  board.reset()
  state = prepare_state(board.squares)
  for moveNum in range(MAX_MOVES):
    # env.render()
    action = agent.act(state)
    next_state, reward, done, winner = step(board, action, player=player)
    agent.remember(state, action, reward, next_state, done)
    state = next_state
    if done: # when episode finished
      # update game stats
      agent.update_target_model()
      if (winner == player):
        stats.won()
      elif winner == enemy:
        stats.lost()
      elif winner == None:
        stats.draw()
      elif winner == WRONG_MOVE:
        stats.illegal_move()
      # put out logs
      print(f"ep: {e}/{EPISODES}, moves: {moveNum}, e: {agent.epsilon:.2}, win/all: {stats.win_rate()} - draws/all {stats.draw_rate()}, winner {winner}")
      board.show()
      break
  # train the DNN when there are enough memories
  if len(agent.memory) > batch_size:
    agent.replay(batch_size)
  # save an snapshot every so often
  if e % 100 == 0:
    agent.save(SAVE_LOC)
