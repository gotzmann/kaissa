import chess
import random
import sys
import argparse
#from movegeneration import next_move
#from uci import uci
#from search import search, best_move, temp_move
#from search import search, best_move, temp_move
#import negamax
from negamax import search
#import resource
import os
import psutil

#process = psutil.Process(os.getpid())
#mem = round(process.memory_info().rss / 1024 / 1024, 2)
#mem1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
#print("MEM1", round(mem, 2), "Mb")
#count = 0

defaultDepth = 2
maxPlies = 4
board = chess.Board()
#board.turn = chess.WHITE
ply = 0
moves = [ 
    chess.Move.from_uci("e2e4"),
    chess.Move.from_uci("d7d5"),
    chess.Move.from_uci("f1b5"),
]

while ply < maxPlies:

    if board.is_game_over():
        print("===============")
        print("   GAME OVER   ")        
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
    #print("MAIN", search.temp_move, search.best_move)
    
    print("\n[", len(list(board.legal_moves)), "] =>", [ move.uci() for move in board.legal_moves ])

#    if ply < len(moves):
#        score = 0
        #search.best_move = moves[ply]
#        search.bestMove = moves[ply]
#    else:    
        #search.best_move = None
        #score = search.negamax(board, defaultDepth, -10000)    
    #score = search.negamax(board, defaultDepth, -10000, 10000)    
    score, move, count = search(board, defaultDepth, -10000, 10000, returnMove = True, returnCount = True)    

    #board.push(search.best_move)   
    board.push(move)   
    ply += 1
    
    print("\n===============")    
    #print(f"# {ply} => {search.best_move} | {score}")
    #print(f"# {ply} => {search.bestMove} | {score}")
    print(f"MOVE {ply} => {move} of {count}")
    print("===============")    
    print(board)
    print("===============")        

#process = psutil.Process(os.getpid())
#mem2 = process.memory_info().rss / 1024 / 1024
#mem2 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
#print("MEM2", mem2, "Mb")
