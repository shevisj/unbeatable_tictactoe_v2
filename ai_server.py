#!/usr/bin/env python
# enable debugging
import cgitb
cgitb.enable()

import cgi
import os
import copy
import random

the_move = 3
player = "O"
opp = "X"

#Returns an array of all available moves in a given board state.
def getPossibleMoves(a_board):
    pMoves = []
    for i in range(0, 9):
        if a_board[i] == "":
            pMoves.append(i)
    return pMoves

#Checks if either X or O has won a given board state.
def checkWon(a_board, symbol):
    if ((a_board[0] == symbol and a_board[1] == symbol and a_board[2] == symbol) or
       (a_board[3] == symbol and a_board[4] == symbol and a_board[5] == symbol) or
       (a_board[6] == symbol and a_board[7] == symbol and a_board[8] == symbol) or
       (a_board[0] == symbol and a_board[3] == symbol and a_board[6] == symbol) or
       (a_board[1] == symbol and a_board[4] == symbol and a_board[7] == symbol) or
       (a_board[2] == symbol and a_board[5] == symbol and a_board[8] == symbol) or
       (a_board[0] == symbol and a_board[4] == symbol and a_board[8] == symbol) or
       (a_board[2] == symbol and a_board[4] == symbol and a_board[6] == symbol)):
          return True
    else:
        return False

#Scoring for minimax algorithm
def score(a_board, depth):
    if checkWon(a_board, player):
        return 10 - depth
    if checkWon(a_board, opp):
        return depth - 10
    else:
        return 0

#returns the index of the max value of an array
def findMaxVal(a_list):
    maxVal = -100
    for i in range(len(a_list)):
        if a_list[i] > maxVal:
            maxVal = a_list[i]
            index = i
    return index

#returns the index of the minimum value of an array
def findMinVal(a_list):
    minVal = 100
    for i in range(len(a_list)):
        if a_list[i] < minVal:
            minVal = a_list[i]
            index = i
    return index

#UNBEATABLE MODE: Calculates and stores every possible game state and sets the_move to be the best possible move for a given board
def Minimax(a_board, value, depth, symbol):
    if checkWon(a_board, player) or checkWon(a_board, opp) or getPossibleMoves(a_board) == []:
        return value
    depth += 1
    scores = []
    moves = getPossibleMoves(a_board)
    newSymbol = copy.deepcopy(symbol)
    if symbol == "X":
        symbol = "O"
    else:
        symbol = "X"

    for i in moves:
        copyBoard = copy.deepcopy(a_board)
        copyBoard[i] = newSymbol
        copyValue = score(copyBoard, depth)
        scores.append(Minimax(copyBoard, copyValue, depth, symbol))

    if newSymbol == player:
        global the_move
        maxScoreIndex = findMaxVal(scores)
        the_move = moves[maxScoreIndex]
        return scores[maxScoreIndex]
    else:
        minScoreIndex = findMinVal(scores)
        return scores[minScoreIndex]


print "Content-type: text/html"
print

d = cgi.parse_qs(os.environ['QUERY_STRING'])
if "board" in d:
    board = str(d["board"][0]).split(',')
    if "p" in d:
        player = str(d["p"][0])
        if player == "X":
            opp = "O"
    if 'X' in board or 'O' in board:
        node = Minimax(board, 0, 0, player)
        print the_move
    else:
        print random.choice([0, 2, 6, 8])
else:
    print "Invalid query string."
