import chess
import random
import sys
import argparse
from negamax import search
#import resource
#import os
#import psutil
import time

start = time.time()

#process = psutil.Process(os.getpid())
#mem = round(process.memory_info().rss / 1024 / 1024, 2)
#mem1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
#print("MEM1", round(mem, 2), "Mb")

tree = ""
defaultDepth = 3
maxPlies = 6
board = chess.Board()

moves = [ 
    chess.Move.from_uci("e2e4"),
    chess.Move.from_uci("d7d5"),
    chess.Move.from_uci("f1b5"),
]
#moves = []
moves = [ 
    chess.Move.from_uci("e2e4"),
    chess.Move.from_uci("d7d5"),
]
moves = []
moves = [ 
    chess.Move.from_uci("d2d4"),
    chess.Move.from_uci("b8c6"),
    chess.Move.from_uci("c1f4"),
]
moves = []
moves = [ 
    chess.Move.from_uci("d2d4"),
    chess.Move.from_uci("b8c6"),
    chess.Move.from_uci("c1f4"),
]
moves = []

while board.ply() < maxPlies:

    if board.is_game_over():
        print("===============")
        print("   GAME OVER   ")        
        print("===============")
        break        
    
    print("\n[", len(list(board.legal_moves)), "] =>", [ move.uci() for move in board.legal_moves ])

    if board.ply() < len(moves):
        score = count = 0
        move = moves[board.ply()]        
    else:    
        score, move, count = search(board, board.turn, defaultDepth, -10000, 10000, returnMove = True, returnCount = True, tree = tree)    

    board.push(move)   
    tree += move.uci() + " | "
    
    print("\n===============")    
    print(f"MOVE {board.ply()} => {move} of {count} => {score}")
    print("===============")    
    print(board)
    print("===============")        

end = time.time()
print("\nTIME", round(end - start, 2), "sec")