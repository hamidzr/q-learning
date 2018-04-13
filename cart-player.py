import random
import gym
import numpy as np
from models.dqn import DQNAgent

EPISODES = 5

env = gym.make('CartPole-v1')
state_size = env.observation_space.shape[0]
action_size = env.action_space.n
agent = DQNAgent(state_size, action_size)
# agent.load("./save/cartpole-ddqn.h5")
done = False
batch_size = 32

for e in range(EPISODES):
  state = env.reset()
  state = np.reshape(state, [1, state_size])
  print(state.shape)
  for time in range(500):
    # env.render()
    action = agent.act(state)
    next_state, reward, done, _ = env.step(action)
    reward = reward if not done else -10
    next_state = np.reshape(next_state, [1, state_size])
    agent.remember(state, action, reward, next_state, done)
    state = next_state
    if done:
      agent.update_target_model()
      print("episode: {}/{}, score: {}, e: {:.2}"
          .format(e, EPISODES, time, agent.epsilon))
      break
  if len(agent.memory) > batch_size:
    agent.replay(batch_size)
# if e % 10 == 0:
#   agent.save("./save/cartpole-ddqn.h5")
