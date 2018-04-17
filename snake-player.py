import numpy as np
from models.dqn import DQNAgent
from games.snake_driver import SnakeDriver
from games.snake import SnakeG
from utils.helpers import GameStats
from models.player import Player

EPISODES = 20000
MAX_MOVES = 10000 # maximum number of moves in a game

# game parameters
BOARD_SIZE=20

# create the game
baseGame = SnakeG(board_size=BOARD_SIZE)
game = SnakeDriver(base_game=baseGame)

# setup the agent
state_size = BOARD_SIZE
action_size = 3 # [left, right, straight]
agent = DQNAgent(state_size, action_size, epsilon=1,
                 epsilon_decay=0.99, epsilon_min=0.01, batch_size=64)

aiPlayer = Player(game=game, max_moves=MAX_MOVES, name='snake-qlearner', agent=agent)


# TODO factor out role from player
aiPlayer.train(episodes=EPISODES, resume=True, save_freq=25, show=False, log='score')
