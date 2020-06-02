#!/usr/local/bin/python3
"""
This is where you should write your AI code!
​
Authors: PLEASE ENTER YOUR NAMES AND USER ID'S HERE
​
Based on skeleton code by Abhilash Kuhikar, October 2019
"""
from logic_IJK import Game_IJK
import math
import copy
import random

# Suggests next move to be played by the current player given the current game
#
# inputs:
#     game : Current state of the game
#
# This function should analyze the current state of the game and determine the
# best move for the current player. It should then call "yield" on that move.

# Heuristics of the Board
def max_tile(board):
 max_tile = 0
 for i in range(6):
   for j in range(6):
     max_tile = max(max_tile,ord(board[i][j]))
 return max_tile

# Static Evaluation Value of the Given Board
def compute_expected_values(board,dete_flag):
    ans = heuristic(board)
    return ans

    # Compute Score to find the next Best Move
#Calculated the smoothness of the current state of the board
def smoothness(board):
    smooth_var = 0
    for i in range(6):
        for j in range(6):
            data = ord(board[i][j])

            if data:
                for row in range(6):
                    smooth_var = abs(data - ord(board[row][j]))
                for col in range(6):
                    smooth_var -= abs(data - ord(board[row][j]))
    return smooth_var

#Calculate the gradient of the current state of the board
def gradient(board):
    gradients = [
        [[5, 4, 3, 2, 1, 0],
         [4, 3, 2, 1, 0, -1],
         [3, 2, 1, 0, -1, -2],
         [2, 1, 0, -1, -2, -3],
         [1, 0, -1, -2, -3,-4],
         [0, -1, -2, -3, -4,-5]],
        [[0, 1, 2, 3, 4, 5],
         [-1, 0, 1, 2, 3, 4],
         [-2, -1, 0, 1, 2, 3],
         [-3, -2, -1, 0, 1, 2],
         [-4, -3, -2, -1, 0, 1],
         [-5, -4, -3, -2, -1, 0]],
        [[0, -1, -2, -3, -4, -5],
         [1, 0, -1, -2, -3, -4],
         [2, 1, 0, -1, -2, -3],
         [3, 2, 1, 0, -1, -2],
         [4, 3, 2, 1, 0 ,-1],
         [0,-1,-2,-3, -4, -5]],
        [[-5, -4, -3, -2, -1, 0],
         [-4, -3, -2, -1, 0, 1],
         [-3, -2, -1, 0, 1, 2],
         [-2, -1,  0, 1, 2, 3],
         [-1, 0 , 1, 2, 3, 4],
         [0, 1, 2, 3, 4, 5]]]

    g_score = [0,0,0,0]

    for g_index in range(4):
        for r in range(6):
            for c in range(6):
                g_score[g_index] += (gradients[g_index][r][c] * ord(board[r][c]))
    return max(g_score)

#Calculate the max tile on the current state of the board
def max_tile_func(board):
  max_tile = 0
  for i in range(6):
    for j in range(6):
      max_tile = max(max_tile,ord(board[i][j]))
  return max_tile

#Calculate the empty tiles
def empty_tiles(B):
   return sum([1 for row in B for char in row if char == ' '])

#Calculate the corner heuristic
def corner_heuristic(board):
  corner_heur = 0
  max_tile = max_tile_func(board)
  #print(max_tile)
  if max_tile == board[5][5] or max_tile == board[0][5] or max_tile == board[0][0] or max_tile ==board[5][0] :
    corner_heur += (max_tile)
  else:
    corner_heur -= (max_tile)
  return corner_heur

#Finally summing up the various heuristic functions
def heuristic(board):
    # Weights assigned to  the various heuristic functions :

    smooth_w = 0.1
    g_weight = 0
    free_weight = 2.5
    max_tile_weight = 0.5
    corner_weight = 0.1

    smooth = smoothness(board) * smooth_w
    grad = gradient(board) * g_weight
    free_Tile = empty_tiles(board) * free_weight
    max_tile = max_tile_func(board) * max_tile_weight
    corner_h = corner_heuristic(board) * corner_weight

    return smooth +free_Tile +grad+ max_tile + corner_h



# Find the Succesor boards of the the Current Board
def succesor_boards(max_player,game,board):
    moves = ['U', 'D', 'L', 'R']
    succs = []
    for move in moves:
        if max_player :
            new_game = Game_IJK(copy.deepcopy(board),"+", game.getDeterministic())
            succ = new_game.makeMove(move)
            succs.append((move,succ.getGame()))
        else:
            new_game = Game_IJK(board, "-", game.getDeterministic())
            succ = new_game.makeMove(move)
            succs.append((move, succ.getGame()))
    return succs

# Compute the Scores of the boards
def compute_score(max_flag,level,limit,board,alpha,beta,game):
    max_values = []
    min_values = []
    final_score = 0
    if max_flag and level < limit:
        boards = succesor_boards(True,game, board)
        for board in boards:
            score = compute_score(False,level + 1,limit,board[1],alpha,beta,game)
            max_values.append(score)
            alpha = max(alpha,score)
            if alpha >= beta:
                break
        return max(max_values)
    elif not max_flag and level < limit:
        boards = succesor_boards(False,game, board)
        for board in boards:
            score = compute_score(True,level + 1,limit,board[1],alpha,beta,game)
            min_values.append(score)
            beta = min(beta,score)
            if alpha >= beta:
                break
        return min(min_values)
    elif max_flag and level == limit:
        return compute_expected_values(board,game.getDeterministic())
    elif not max_flag and level == limit:
        return compute_expected_values(board,game.getDeterministic())

    return final_score

def next_move(game: Game_IJK)-> None:

    '''board: list of list of strings -> current state of the game
           current_player: int -> player who will make the next move either ('+') or -'-')
           deterministic: bool -> either True or False, indicating whether the game is deterministic or not
    '''
    global InitialPlayer
    InitialPlayer = game.getCurrentPlayer()
    board = game.getGame()
    player = game.getCurrentPlayer()
    deterministic = game.getDeterministic()

    # You'll want to put in your fancy AI code here. For right now this just
    boards = []
    level = 0
    max_score = -math.inf
    min_score = math.inf
    final_move = ""
    if player == "+":
        boards = succesor_boards(True,game,board)
    else:
        boards = succesor_boards(False, game, board)

    for board in boards:
        alpha = -math.inf
        beta = math.inf
        score = compute_score(False, level, 3, board[1], alpha, beta, game)
        if score > max_score:
            # print(score)
            # print("Final score")
            max_score = score
            final_move = board[0]
    yield final_move
