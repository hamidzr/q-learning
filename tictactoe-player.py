import numpy as np
from models.dqn import DQNAgent
from games.tictactoe_driver import TicTacToe
from games.tictactoe import Tic, get_enemy
from utils.helpers import GameStats

EPISODES = 20000
MAX_MOVES = 100 # maximum number of moves in a game
SAVE_LOC = "weights/tictactoe-ddqn.h5"

# create the game
board = Tic(random_ratio=0.1)
game = TicTacToe(base_game=board)

# setup the agent
state_size = 9
action_size = state_size
agent = DQNAgent(state_size, action_size, epsilon=0.05,
                 epsilon_decay=0.995, epsilon_min=0.01, batch_size=32)
agent.load(SAVE_LOC)


# game stats
stats = GameStats()
done = False


player = 'X'
enemy = get_enemy(player)


# TODO more exploration?
for e in range(EPISODES):
  game.reset()
  state = game.state()
  for moveNum in range(MAX_MOVES):
    # env.render()
    action = agent.act(state)
    next_state, reward, done, winner = game.step(action, player)
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
      elif winner == game._game.WRONG_MOVE:
        stats.illegal_move()
      # put out logs
      print(f"ep: {e}/{EPISODES}, moves: {moveNum}, e: {agent.epsilon:.2}, win/all: {stats.win_rate()} - draws/all {stats.draw_rate()}, winner {winner}")
      game.show()
      break
  # train the DNN if there are enough memories
  agent.attempt_replay()
  # save an snapshot every so often
  # if e % 100 == 0:
  #   agent.save(SAVE_LOC)
