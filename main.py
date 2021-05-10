import chess
import random
import sys
import argparse
#from negamax import search
from parallel import search
#import resource
#import os
#import psutil
import time
import copy
from multiprocessing import Pool

# TODO Compute Moves Per Second metric to understand the average performance
# TODO no castling
# TODO no enpassant
# TODO no 3 fold repetition
# TODO no 50 rule move count

start = time.time()

#process = psutil.Process(os.getpid())
#mem = round(process.memory_info().rss / 1024 / 1024, 2)
#mem1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
#print("MEM1", round(mem, 2), "Mb")

defaultDepth = 4
if len(sys.argv) > 1:
    defaultDepth = int(sys.argv[1])
#print(defaultDepth)
#sys.exit()

tree = ""
maxPlies = 0 # zero for unlimited moves
movesPerSecond = 0
board = chess.Board()
boards = [] # we should check for 3-fold repetition and similar things

# Test multiprocessing

def choose(result):
    print("=== CHOOSE ===")
    print(result)
    print("=== \CHOOSE ===")

def para(move):
    print("PARA", move)
#    print(board.push(move))  
    return move

print("NAME |", __name__)

# Child processes have names: __mp_main__
if __name__ == "__main__":

#    print("IF MAIN")
    
    moves = list(board.legal_moves)
    pool = Pool(len(moves))
#    results = []

    #for move in board.legal_moves:   
    #    print(move) 
    #    newBoard = copy.deepcopy(board)
    #    newBoard.push(move)
        #args = (newBoard)
    #results.append({ 
    #    "move": move.uci(), 
        #"score": pool.apply_async(para, args = (newBoard), callback = choose),
    #    "score": pool.map(para, board.legal_moves),
    #}) 

    #res = pool.map(workers.para, board.legal_moves)
    ###res = pool.map_async(paramain, [1, 2, 3])
    res = pool.map_async(para, moves)
#    print(res.get())

    pool.close()
    pool.join()

#    for result in results:
#        result["score"].wait()
#    print("SLEEP 10")
#    time.sleep(10)
    print(res.get())
#    for result in results:
#        print(result["move"], "=>", result["score"].get())

#    print("FINALLY")
#    print(results)

#    pool.join()    
#    print("MAIN SLEEP 1 AND DIE")
    #sys.exit()

#print("SLEEP 1 AND DIE")
#time.sleep(1)
#sys.exit()

