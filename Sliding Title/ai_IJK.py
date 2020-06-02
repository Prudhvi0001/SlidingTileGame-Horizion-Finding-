#!/usr/local/bin/python3

"""
This is where you should write your AI code!

Authors: Naga Anjaneyulu,Prudhvi Vajja, Ruthvik Parvat

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



# Static Evaluation Value of the Given Board
def compute_expected_values(board,dete_flag,initialturn):
    upper = 0
    lower = 0
    B = board
    for i in range(len(B)):
        for j in range(len(B[0])):
            if B[i][j].isupper():
                if i - 1 >= 0 and i + 1 < 6 and j - 1 >= 0 and j + 1 < 6:
                    if B[i][j] == B[i - 1][j].upper():
                        upper += pow(2, ord(B[i][j]) - ord("@"))
                    if B[i][j] == B[i + 1][j].upper():
                        upper += pow(2, ord(B[i][j]) - ord("@"))
                    if B[i][j] == B[i][j - 1].upper():
                        upper += pow(2, ord(B[i][j]) - ord("@"))
                    if B[i][j] == B[i][j + 1].upper():
                        upper += pow(2, ord(B[i][j]) - ord("@"))
            elif B[i][j].islower():
                if i - 1 >= 0 and i + 1 < 6 and j - 1 >= 0 and j + 1 < 6:
                    if B[i][j] == B[i - 1][j].lower():
                        lower += pow(2, ord(B[i][j]) - ord("`"))
                    if B[i][j] == B[i + 1][j].lower():
                        lower += pow(2, ord(B[i][j]) - ord("`"))
                    if B[i][j] == B[i][j - 1].lower():
                        lower += pow(2, ord(B[i][j]) - ord("`"))
                    if B[i][j] == B[i][j + 1].lower():
                        lower += pow(2, ord(B[i][j]) - ord("`"))
    upper1 = sum([pow(2,abs(ord(char) - ord("@"))) for row in board for char in row if char.isupper()])
    lower1 = sum([pow(2,abs(ord(char) - ord("`"))) for row in board for char in row if char.islower()])
    empty_tiles = sum([1 for row in board for char in row if char == ' '])
    if initialturn == '+':
        return (upper - lower + upper1 - lower1)+empty_tiles
    else:
        return (lower - upper + lower1 - upper1)+empty_tiles


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
            new_game = Game_IJK(copy.deepcopy(board), "-", game.getDeterministic())
            succ = new_game.makeMove(move)
            succs.append((move, succ.getGame()))
    return succs

def chance_boards(max_player,game,board,move,empty_tiles):
    succs =[]
    for i in range(0,empty_tiles):
         if max_player :
            new_game = Game_IJK(copy.deepcopy(board),"+", game.getDeterministic())
            succ = new_game.makeMove(move)
            succs.append((move,succ.getGame()))
         else:
            new_game = Game_IJK(copy.deepcopy(board), "-", game.getDeterministic())
            succ = new_game.makeMove(move)
            succs.append((move, succ.getGame()))
    return succs
 


def get_empty_tiles(board):
    return sum([1 for row in board for char in row if char == ' '])
       
    

# Compute the Scores of the boards
def compute_score(chance_flag,max_flag,level,limit,board,alpha,beta,game,ourturn,move):
    max_values = []
    min_values = []
    chance_values = []
    final_score = 0
    moves = ['U', 'D', 'L', 'R']
    if chance_flag and level < limit:
        empty_tiles =  get_empty_tiles(board)
        boards = chance_boards(max_flag,game,board,move,empty_tiles)
        for board in boards:
            score = compute_score(False,not max_flag,level + 1,limit,board[1],alpha,beta,game,ourturn,"")
            chance_values.append(score)
            if max_flag:
                alpha = max(alpha,score)
            else:
                beta = min(beta,score)
            if alpha >= beta:
                break
        return sum(chance_values)/len(chance_values)
    elif max_flag and level < limit:
        "Max Node "
        if game.getDeterministic():
            boards = succesor_boards(True,game, board)
            for board in boards:
                score = 0
                score = compute_score(False,False,level + 1,limit,board[1],alpha,beta,game,ourturn,"")
                max_values.append(score)
                alpha = max(alpha,score)
                if alpha >= beta:
                    break
            return max(max_values)
        else:
            avg_scores =[]
            for move in moves:
                score = compute_score(True,True,level + 1,limit,board,alpha,beta,game,ourturn,move)
                avg_scores.append(score)
                alpha = max(alpha,score)
                if alpha >= beta:
                    break
            return max(avg_scores)
    elif not max_flag and level < limit:
        " Min Node "
        if game.getDeterministic():
            boards = succesor_boards(False,game, board)
            for board in boards:
                score = compute_score(False,True,level + 1,limit,board[1],alpha,beta,game,ourturn,"")
                beta = min(beta,score)
                min_values.append(score)
                if alpha >= beta:
                    break
            return min(min_values)
        else:
            avg_scores = []    
            for move in moves:
                score = compute_score(True,False,level + 1,limit,board,alpha,beta,game,ourturn,move)
                beta = min(beta,score)
                avg_scores.append(score)
                if alpha >= beta:
                    break
            return min(avg_scores)
    
    elif chance_flag and level == limit:
        chance_values =[]
        empty_tiles =  get_empty_tiles(board)
        boards = chance_boards(max_flag,game,board,move,empty_tiles)
        for board in boards:
            score = compute_expected_values(board[1],game.getDeterministic(),ourturn)
            chance_values.append(score)
        return sum(chance_values)/len(chance_values)
    else:
        if max_flag and level == limit:
            return compute_expected_values(board,game.getDeterministic(),ourturn)
        if not max_flag and level == limit:
            return compute_expected_values(board,game.getDeterministic(),ourturn)

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
    if deterministic :
        " Minimax  - alpha/beta pruning"
        if player == "+":
             boards = succesor_boards(True,game,board)
        else:
            boards = succesor_boards(False, game, board)
        for board in boards:
            alpha = -math.inf
            beta = math.inf
            score = compute_score(False,False, level, 3, board[1], alpha, beta, game,InitialPlayer,"")
            if score > max_score:
                # print(score)
                # print("Final score")
                max_score = score
                final_move = board[0]
       
    else:
        " Expectiminimax - alpha/beta pruning"
        moves = ['U', 'D', 'L', 'R']
        empty_tiles = get_empty_tiles(board)
        for move in moves :
                 score = 0
                 if player == "+":
                     boards = chance_boards(True,game,board,move,empty_tiles)
                 else:
                     boards = chance_boards(False, game,board,move,empty_tiles)
                 for board1 in boards:
                     alpha = -math.inf
                     beta = math.inf
                     score += compute_score(False,False, level, 3, board1[1], alpha, beta, game,InitialPlayer,"")
                 avg_score = score/empty_tiles
                 if avg_score > max_score:
                     # print(score)
                     # print("Final score")
                     max_score = avg_score
                     final_move = move
                        
     
    yield final_move

        
      








