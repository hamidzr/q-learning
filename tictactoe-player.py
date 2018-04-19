import numpy as np
from models.dqn import DQNAgent
from games.tictactoe_driver import TicTacToe
from games.tictactoe import Tic, get_enemy
from utils.helpers import GameStats
from models.player import Player

EPISODES = 20000
MAX_MOVES = 100 # maximum number of moves in a game
SAVE_LOC = "weights/tictactoe-ddqn.h5"

# create the game
board = Tic(random_ratio=0.4)
game = TicTacToe(base_game=board)

# setup the agent
state_size = 9
action_size = state_size
agent = DQNAgent(state_size, action_size, epsilon=0.05,
                 epsilon_decay=0.995, epsilon_min=0.01, batch_size=32)
# agent.load(SAVE_LOC)

aiPlayer = Player(game=game, max_moves=MAX_MOVES, name='tic-qlearner', agent=agent, role='X')

# TODO factor out role from player
aiPlayer.train(episodes=EPISODES, resume=False, show=False)
