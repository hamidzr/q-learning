import random
import numpy as np
import os
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K

class DQNAgent:
  def __init__(self, state_size, action_size, epsilon=1,
               epsilon_min=0.01, epsilon_decay=0.99,
               discount_rate=0.95, learning_rate=0.001,
               batch_size=32, memory_length=2000):
    self.batch_size = batch_size
    self.state_size = state_size
    self.action_size = action_size
    self.memory = deque(maxlen=memory_length)
    self.gamma = discount_rate  # discount rate
    self.epsilon = float(epsilon)  # exploration rate
    self.epsilon_min = epsilon_min
    self.epsilon_decay = epsilon_decay
    self.learning_rate = learning_rate
    self.model = self._build_model()
    self.target_model = self._build_model()
    self.update_target_model()

  def _huber_loss(self, target, prediction):
    # sqrt(1+error^2)-1
    error = prediction - target
    return K.mean(K.sqrt(1+K.square(error))-1, axis=-1)

  def _build_model(self):
    # Neural Net for Deep-Q learning Model
    model = Sequential()
    model.add(Dense(24, input_dim=self.state_size, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(self.action_size, activation='linear'))
    model.compile(loss=self._huber_loss,
            optimizer=Adam(lr=self.learning_rate))
    return model

  def update_target_model(self):
    # copy weights from model to target_model
    self.target_model.set_weights(self.model.get_weights())

  def remember(self, state, action, reward, next_state, done):
    self.memory.append((state, action, reward, next_state, done))

  def act(self, state):
    if np.random.rand() <= self.epsilon:
      return random.randrange(self.action_size)
    act_values = self.model.predict(state)
    return np.argmax(act_values[0])  # returns action

  def attempt_replay(self):
    if len(self.memory) > self.batch_size: self.replay()

  def replay(self):
    minibatch = random.sample(self.memory, self.batch_size)
    # print('minibatch shape', minibatch[0])
    for state, action, reward, next_state, done in minibatch:
      # print('state shape', state.shape)
      target = self.model.predict(state)
      if done:
        target[0][action] = reward
      else:
        a = self.model.predict(next_state)[0]
        t = self.target_model.predict(next_state)[0]
        target[0][action] = reward + self.gamma * t[np.argmax(a)]
      self.model.fit(state, target, epochs=1, verbose=0)
    if self.epsilon > self.epsilon_min:
      # TODO linear decay?
      self.epsilon *= self.epsilon_decay

  def load(self, name):
    if os.path.isfile(name):
      self.model.load_weights(name)
    else:
      print(f'{name} does not exist, skipped loading.')

  def save(self, name):
    print('saving', name)
    self.model.save_weights(name)
