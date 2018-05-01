import random
from utils.helpers import args
from models.player import Player
import gym
from games.cart_driver import GameDriver
import numpy as np
from models.dqn import DQNAgent

EPISODES = 1000
MAX_MOVES = 500
memory_size = 2000

baseGame = gym.make('CartPole-v1')
game = GameDriver(base_game=baseGame)

state_size = baseGame.observation_space.shape[0]
action_size = baseGame.action_space.n

agent = DQNAgent(state_size, action_size, epsilon=args.start_epsilon,
                 epsilon_decay=0.99, epsilon_min=0.10, batch_size=32, memory_length=memory_size)

aiPlayer = Player(game=game, max_moves=MAX_MOVES, name='cart-qlearner', agent=agent, log='score')

aiPlayer.train(episodes=EPISODES, resume=args.save_resume, save_freq=args.save_freq, show=args.show, plot_freq=args.plot_freq, update_freq=1)
