import numpy as np
from models.dqn import DQNAgent
from games.tictactoe_driver import TicTacToe
from games.tictactoe import Tic, get_enemy
from utils.helpers import GameStats
from models.player import Player
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--show", type=bool, default=False, help="show game progress")
parser.add_argument("--save_resume", type=bool, default=False, help="save and resume?")
args = parser.parse_args()


EPISODES = 20000
MAX_MOVES = 100 # maximum number of moves in a game

# create the game
board = Tic(random_ratio=0.4)
game = TicTacToe(base_game=board)

# setup the agent
state_size = 9
action_size = state_size
agent = DQNAgent(state_size, action_size, epsilon=1,
                 epsilon_decay=0.995, epsilon_min=0.01, batch_size=32)

aiPlayer = Player(game=game, max_moves=MAX_MOVES, name='tic-qlearner', agent=agent, role='X')

aiPlayer.train(episodes=EPISODES, resume=args.save_resume, show=args.show)
