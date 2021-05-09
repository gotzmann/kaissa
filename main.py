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
maxPlies = 222
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

# Scholar's mate
moves = [ 
    chess.Move.from_uci("e2e4"),
    chess.Move.from_uci("e7e5"),
    chess.Move.from_uci("d1h5"),
    chess.Move.from_uci("b8c6"),
    chess.Move.from_uci("f1c4"),    
    chess.Move.from_uci("g8f6"),
]
#print(moves)
#sys.exit()

moves = "f2f4 d7d5 e2e3 b8c6 f1b5 d8d6 b1c3 e7e6 d2d4 g8f6 d1d3 h8g8 g1f3 e8d8 f3g5 d8e8 g5h7 f6h7 d3h7 a7a6 b5c6 d6c6 h7g8 c6c4 e1f2 f7f5 g8h7 e8d7 h7g8 f8e7 g8g7 c7c5 d4c5 c4c5 f2f3 d7c6 g7d4 c5a5 d4a4 a5a4 c3a4 e7d6 a4c3 a8a7 h1d1 d6c5 c3a4 c5d6 d1d3 b7b6 d3b3 a7b7 b3d3 c6d7 c2c4 d5c4 d3d4 d7e7 d4c4 d6c7 a4b6 c7b6 c4c8 e7d6 c8a8 d6d5 a8a6 b7b8 a6a3 b8g8 a3d3 d5c6 e3e4 f5e4 f3e4 g8g2 d3d2 g2d2 c1d2 c6d6 d2c3 d6c6 c3e5 c6b7 a1d1 b7c8 d1d6 b6c7 d6c6 c8b7 c6c7 b7b6 c7e7 b6c6 e7e6 c6b5 e5d4 b5b4 e6b6"
moves = moves.split()
moves = [ chess.Move.from_uci(move) for move in moves ]
#print(moves)
#sys.exit()

if len(moves):
    print("PERFORM", len(moves), "plies from MOVES list")

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