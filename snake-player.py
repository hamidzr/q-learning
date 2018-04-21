import numpy as np
from models.dqn import DQNAgent
from games.snake_driver import SnakeDriver
from games.snake import SnakeG
from utils.helpers import GameStats, args
from models.player import Player


EPISODES = 20000
MAX_MOVES = 500 # maximum number of moves in a game

# game parameters
BOARD_SIZE=5

# create the game
baseGame = SnakeG(board_size=BOARD_SIZE, grow=False, initial_snake=[(0,0)])
game = SnakeDriver(base_game=baseGame, log='score')
game.test()

# setup the agent # REMEMBER set correct state size, state has to be flat (1,)
state_size = game.state().shape[1]
action_size = 3 # [left, right, straight]
agent = DQNAgent(state_size, action_size, epsilon=args.start_epsilon,
                 epsilon_decay=0.995, epsilon_min=0.01, batch_size=32)

aiPlayer = Player(game=game, max_moves=MAX_MOVES, name='snake-qlearner', agent=agent)


aiPlayer.train(episodes=EPISODES, resume=args.save_resume, save_freq=100, show=args.show)
