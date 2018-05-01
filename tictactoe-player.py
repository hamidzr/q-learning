import numpy as np
from models.dqn import DQNAgent
from games.tictactoe_driver import TicTacToe
from games.tictactoe import Tic, get_enemy
from utils.helpers import GameStats, args
from models.player import Player


EPISODES = 20000
MAX_MOVES = 100 # maximum number of moves in a game

# create the game
board = Tic(random_ratio=0.1)
game = TicTacToe(base_game=board)

# setup the agent
STATE_SIZE = game.state().shape[1]
ACTION_SIZE = 9
agent = DQNAgent(STATE_SIZE, ACTION_SIZE, epsilon=args.start_epsilon,
                 epsilon_decay=0.995, epsilon_min=0.01, batch_size=32)

aiPlayer = Player(game=game, max_moves=MAX_MOVES, name='tic-qlearner', agent=agent, role='X')

aiPlayer.train(episodes=EPISODES, resume=args.save_resume, show=args.show, plot_freq=args.plot_freq)
