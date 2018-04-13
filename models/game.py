from abc import ABC, abstractmethod

# a wrapper abstract class to help prepare the game for learning
# abstrat methods must be present on the children
class Game(ABC):
  def __init__(self):
    super(Game, self).__init__()

  @abstractmethod
  def state(self):
    pass

  @abstractmethod
  def step(self):
    # new_state, reward, isDone, info
    pass

  @abstractmethod
  def show(self):
    pass

  @abstractmethod
  def reset(self):
    pass
