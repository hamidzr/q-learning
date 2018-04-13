#!/usr/bin/env python

import random
import numpy as np


class Tic:
  winning_combos = (
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6])

  winners = ('X-win', 'Draw', 'O-win')

  def __init__(self, squares=[], random_ratio=0):
    self.random_ratio=random_ratio
    if len(squares) == 0:
      self.squares = [None for i in range(9)]
    else:
      self.squares = squares

  def reset(self):
    self.squares = [None for i in range(9)]

  def show(self):
    for element in [self.squares[i:i + 3] for i in range(0, len(self.squares), 3)]:
      print(element)

  def available_moves(self):
    """what spots are left empty?"""
    return [k for k, v in enumerate(self.squares) if v is None]

  def available_combos(self, player):
    """what combos are available?"""
    return self.available_moves() + self.get_squares(player)

  def complete(self):
    """is the game over?"""
    if None not in [v for v in self.squares]:
      return True
    if self.winner() != None:
      return True
    return False

  def X_won(self):
    return self.winner() == 'X'

  def O_won(self):
    return self.winner() == 'O'

  def tied(self):
    return self.complete() == True and self.winner() is None

  def winner(self):
    for player in ('X', 'O'):
      positions = self.get_squares(player)
      for combo in self.winning_combos:
        win = True
        for pos in combo:
          if pos not in positions:
            win = False
        if win:
          return player
    return None

  def get_squares(self, player):
    """squares that belong to a player"""
    return [k for k, v in enumerate(self.squares) if v == player]

  def make_move(self, position, player):
    """place on square on the board"""
    self.squares[position] = player

  def alphabeta(self, node, player, alpha, beta):
    if node.complete():
      if node.X_won():
        return -1
      elif node.tied():
        return 0
      elif node.O_won():
        return 1
    for move in node.available_moves():
      node.make_move(move, player)
      val = self.alphabeta(node, get_enemy(player), alpha, beta)
      node.make_move(move, None)
      if player == 'O':
        if val > alpha:
          alpha = val
        if alpha >= beta:
          return beta
      else:
        if val < beta:
          beta = val
        if beta <= alpha:
          return alpha
    if player == 'O':
      return alpha
    else:
      return beta

  # play against an AI. a response move will be made by the AI
  def move_and_respond(self, move, player='X'):
    self.make_move(move, player)
    if not self.complete():
      enemy_player = get_enemy(player)
      computer_move = determine(self, enemy_player, random_ratio=self.random_ratio)
      self.make_move(computer_move, enemy_player)
    return self.squares

  # standard interface to the game (apply action, get state)
  def state(self):
    state = self.squares[:] # make a copy
    # map x and o to numbers
    for idx, val in enumerate(state):
    # TODO normalize values (0,1)
      if val == 'O':
        state[idx] = 1
      if val == 'X':
        state[idx] = -1
      if val == None:
        state[idx] = 0
    return np.array(state).reshape(1, len(state))

# assuming that the player is 'X'
  def step(self, action, player='X'):
    # next_state, reward, done = env.step(action)
    if not action in self.available_moves():
      new_state = self.state()
      reward = -1
      done = False
      return new_state, reward, done
    # prepare the new_state
    self.move_and_respond(action, player=player)
    new_state = self.state()
    # what is the reward
    winner = self.winner()
    if winner ==  player:
      reward = 10
    elif winner == get_enemy(player):
      reward = -10
    else:
      reward = -0.5 # or 0?
    reward = float(reward)

    # is it finished?
    done = self.complete() # OPTIMIZE recomputing the winner
    return new_state, reward, done



def determine(board, player, random_ratio=0):
  a = -2
  choices = []
  if len(board.available_moves()) == 9:
    return 4
  if random.uniform(0,1) < random_ratio:
    return random.choice(board.available_moves())
  for move in board.available_moves():
    board.make_move(move, player)
    val = board.alphabeta(board, get_enemy(player), -2, 2)
    board.make_move(move, None)
    # print("move:", move + 1, "causes:", board.winners[val + 1])
    if val > a:
      a = val
      choices = [move]
    elif val == a:
      choices.append(move)
  return random.choice(choices)


def get_enemy(player):
  if player == 'X':
    return 'O'
  return 'X'

if __name__ == "__main__":
  board = Tic()
  board.show()

  while not board.complete():
    player = 'X'
    player_move = int(input("Next Move: "))
    if not player_move in board.available_moves():
      continue
    board.move_and_respond(player_move, player, difficulty=0.5)
    board.show()
    if board.complete():
      break
  print("winner is", board.winner())
