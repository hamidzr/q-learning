import numpy as np
from models.dqn import DQNAgent
from games.tictactoe import Tic

EPISODES = 5000

board = Tic(random_ratio=0.9)
state_size = 9
action_size = state_size
agent = DQNAgent(state_size, action_size)
# agent.load("./save/cartpole-ddqn.h5")
done = False
batch_size = 16

for e in range(EPISODES):
  board.reset()
  state = board.state()
  for moveNum in range(100):
    # env.render()
    action = agent.act(state)
    next_state, reward, done = board.step(action)
    agent.remember(state, action, reward, next_state, done)
    state = next_state
    if done:
      agent.update_target_model()
      print("episode: {}/{}, moveCount: {}, e: {:.2}, winner {}"
          .format(e, EPISODES, moveNum, agent.epsilon, board.winner()))
      break
  if len(agent.memory) > batch_size:
    agent.replay(batch_size)
  # if e % 50 == 0:
  #   agent.save("./save/cartpole-ddqn.h5")
