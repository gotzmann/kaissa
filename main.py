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
#import os
#import psutil
import time

start = time.time()

#process = psutil.Process(os.getpid())
#mem = round(process.memory_info().rss / 1024 / 1024, 2)
#mem1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
#print("MEM1", round(mem, 2), "Mb")
#count = 0

tree = ""
defaultDepth = 3
maxPlies = 6
board = chess.Board()
#board.turn = chess.WHITE

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

while board.ply() < maxPlies:

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
    
    print("\n[", len(list(board.legal_moves)), "] =>", [ move.uci() for move in board.legal_moves ])

    if board.ply() < len(moves):
        score = count = 0
        move = moves[ply]        
    else:    
        #search.best_move = None
        #score = search.negamax(board, defaultDepth, -10000)    
        #score = search.negamax(board, defaultDepth, -10000, 10000)    
        score, move, count = search(board, board.turn, defaultDepth, -10000, 10000, returnMove = True, returnCount = True, tree = tree)    
#    score, move, count = search(board, defaultDepth, -10000, 10000, returnMove = True, returnCount = True)    

    #board.push(search.best_move)   
    board.push(move)   
    tree += move.uci() + " | "
    
    print("\n===============")    
    #print(f"# {ply} => {search.best_move} | {score}")
    #print(f"# {ply} => {search.bestMove} | {score}")
    print(f"MOVE {board.ply()} => {move} of {count} => {score}")
    print("===============")    
    print(board)
    print("===============")        

#process = psutil.Process(os.getpid())
#mem2 = process.memory_info().rss / 1024 / 1024
#mem2 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
#print("MEM2", mem2, "Mb")

end = time.time()
print("\nTIME", round(end - start, 2), "sec")