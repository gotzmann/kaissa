import chess
import random
import sys
import argparse
#from movegeneration import next_move
#from uci import uci
from search import search

defaultDepth = 1
maxPlies = 2

board = chess.Board()
ply = 0

#while not board.is_checkmate():
while ply <= maxPlies:

    if board.is_game_over():
        #ply = step
        #print("\n---------------")
        #print(i + 1, "=>", move)
        #print("---------------")    
        #print(board)
        #print("---------------")    
        print("!CHECK'N'МАТE!")
        print("---------------")
        break        

    # Make evaluated move for whites and just any random for blacks
    if board.turn == chess.WHITE:
        move = search(board, defaultDepth, -100000)
    else:
        if ply == 1:
            move = chess.Move(chess.B7, chess.B5)
        else:    
            moves = list(board.legal_moves)
            move = random.choice(moves)

    board.push(move)   
    ply += 1

    print("\n---------------")
    print("#", ply, "=>", move)
    print("---------------")    
    print(board)
    print("---------------")    
