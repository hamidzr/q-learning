import numpy as np
from models.dqn import DQNAgent
from games.connectn_driver import Driver
from games.connectn import Game, RED, YELLOW
from models.player import Player
from utils.helpers import args

EPISODES = 20000
MAX_MOVES = 20 # maximum number of moves in a game

# game parameters
COLS=5
ROWS=6

# create the game
baseGame = Game(cols=COLS, rows=ROWS)
game = Driver(base_game=baseGame)
game.test()

# setup the agent # REMEMBER set correct state size, state has to be flat (1,)
state_size = game.state().shape[1]
action_size = COLS # [left, right, straight]
agentRed = DQNAgent(state_size, action_size, epsilon=1,
                    epsilon_decay=0.99, epsilon_min=0.01, batch_size=32)

redPlayer = Player(game=game, max_moves=MAX_MOVES,
                   name='connectn-red-qlearner', agent=agentRed,
                   role=RED, log='wins')


agentYellow = DQNAgent(state_size, action_size, epsilon=1,
                       epsilon_decay=0.99, epsilon_min=0.1, batch_size=32)

yellowPlayer = Player(game=game, max_moves=MAX_MOVES,
                      name='connectn-yellow-qlearner', agent=agentYellow,
                      role=YELLOW, log='wins')

# TODO factor out role from player
redPlayer.train(episodes=EPISODES, resume=args.save_resume, save_freq=100, show=args.show, opponent=yellowPlayer)
