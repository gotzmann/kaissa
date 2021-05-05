import chess
import random
import sys
import argparse
#from movegeneration import next_move
#from uci import uci
#from search import search, best_move, temp_move
#from search import search, best_move, temp_move
import search
#import resource
import os
import psutil

process = psutil.Process(os.getpid())
mem = round(process.memory_info().rss / 1024 / 1024, 2)
#mem1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print("MEM1", round(mem, 2), "Mb")
#count = 0

defaultDepth = 1
maxPlies = 4
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

    #score, move = search(board, defaultDepth, -10000)
    score = search.negamax(board, defaultDepth, -10000)

    print("MAIN", search.temp_move, search.best_move)

    board.push(search.best_move)   
    ply += 1

    print("\n===============")    
    print("#", ply, "=>", search.best_move, "|", score)
    print("===============")    
    print(board)
    print("===============")        

process = psutil.Process(os.getpid())
mem2 = process.memory_info().rss / 1024 / 1024
#mem2 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print("MEM2", mem2, "Mb")
