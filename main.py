import chess
import random
import sys
import argparse
#from movegeneration import next_move
#from uci import uci
from search import search

defaultDepth = 4
maxPlies = 6
board = chess.Board()
#board.turn = chess.WHITE
ply = 0

while ply < maxPlies:

    if board.is_game_over():
        print("===============")
        print("   CHECKМАТE   ")        
        print("===============")
        break        

    # Make evaluated move for whites and just any random for blacks
    ###if board.turn == chess.WHITE:
        ###score, move = search(board, defaultDepth, -10000, None)
        #print(score)
        #print(move)
        #move = chess.Move(chess.B7, chess.B5)
        #print(move)
    ###else:
    ###    if ply == 1:
    ###        move = chess.Move(chess.B7, chess.B5)
    ###    else:    
            #moves = list(board.legal_moves)
            #move = random.choice(moves)
    ###        score, move = search(board, defaultDepth, -10000, None)

    score, move = search(board, defaultDepth, -10000, None)
    board.push(move)   
    ply += 1

    print("\n===============")    
    print("#", ply, "=>", move)
    print("===============")    
    print(board)
    print("===============")        
