import numpy as np
from models.dqn import DQNAgent
from games.tictactoe import *

EPISODES = 20000
SAVE_LOC = "weights/tictactoe-ddqn.h5"

board = Tic(random_ratio=0.1)
state_size = 9
action_size = state_size
batch_size = 16
agent = DQNAgent(state_size, action_size, epsilon=0.05, epsilon_decay=0.995, epsilon_min=0.01)
agent.load(SAVE_LOC)

wins = 1
losses = 1
draws = 1
bad_moves = 1
player = 'X'
done = False
enemy = get_enemy(player)

def total_games():
  return wins + losses + draws

def win_rate():
  return round(wins/total_games(), 2)

def draw_rate():
  return round(draws/total_games(), 2)

# TODO more exploration?
for e in range(EPISODES):
  board.reset()
  state = board.state()
  for moveNum in range(100):
    # env.render()
    action = agent.act(state)
    next_state, reward, done, winner = board.step(action, player=player)
    agent.remember(state, action, reward, next_state, done)
    state = next_state
    if done:
      agent.update_target_model()
      if (winner == player):
        wins += 1
      elif winner == enemy:
        losses += 1
      elif winner == None:
        draws += 1
      elif winner == WRONG_MOVE:
        bad_moves += 1
      print(f"ep: {e}/{EPISODES}, moves: {moveNum}, e: {agent.epsilon:.2}, win/all: {win_rate()} - draws/all {draw_rate()}, winner {winner}")
      board.show()
      break
  if len(agent.memory) > batch_size:
    agent.replay(batch_size)
  if e % 100 == 0:
    agent.save(SAVE_LOC)
