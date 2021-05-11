import chess
#import random
import sys
#import argparse
#from negamax import search
from parallel import search, startWorkers, stopWorkers
#import parallel
#import resource
#import os
#import psutil
import time
import copy

# TODO Remove turn parameter for negamax and evaluate functions
# TODO Compute count correctly

# TODO Compute Moves Per Second metric to understand the average performance
# TODO no castling
# TODO no enpassant
# TODO no 3 fold repetition
# TODO no 50 rule move count

#print(__name__)

def main():    

    startWorkers() # Init multiprocessing

    start = time.time()

    maxPlies = 5 # zero for unlimited moves
    defaultDepth = 5
    if len(sys.argv) > 1:
        defaultDepth = int(sys.argv[1])

    tree = ""
    movesPerSecond = 0
    board = chess.Board()
    boards = [] # we should check for 3-fold repetition and similar things

    moves = []
        
    while not maxPlies or board.ply() < maxPlies:

        if board.is_game_over():
            print("===============")
            print("   GAME OVER   ")
            print("     ", board.outcome().result())        
            print("===============")
            break        

        print("\n[", len(list(board.legal_moves)), "] =>", [ move.uci() for move in board.legal_moves ])

        if board.ply() < len(moves):
            score = count = 0
            move = moves[board.ply()]        
        else:    
            ###################score, move, count = search(board, board.turn, defaultDepth, -10000, 10000, returnMove = True, returnCount = True, tree = tree)    
            #move, score, count = search(board, defaultDepth, -10000, 10000)    
            move, score, count = search(board, board.turn, defaultDepth, -10000, 10000)    

        board.push(move)   
        #tree += move.uci() + " | "
        tree = ">> "
        movesPerSecond += count

        print("\n===============")    
        #print(f"MOVE {board.ply()} => {move} of {count} => {score}")
        #print(f"MOVE {board.ply()} => {move} of {count}")
        print(f"MOVE {board.ply()} => {move} of {count} => {score}")
        print("===============")    
        print(board)
        print("===============")        

        # Check for 3-fold rule
        # TODO Store hash of FEN strings to speed up things
        boards.append(copy.copy(board))
        if len(boards) > 8:
            folds = 1
            #for i, b in enumerate(boards[::-1]):
            # Traverse over all previous board states from the one before the current and calculate repetitions
            for b in boards[-2:-10:-1]:
                if board.board_fen() == b.board_fen():
                    folds += 1

            if folds == 3:
                print("===============")
                print("    3-FOLD!    ")        
                print("===============")
                break

    end = time.time()
    execTime = end - start

    stopWorkers()

    print("\n[TIME]", round(execTime, 2), "sec")
    print("[MPS]", round(movesPerSecond / execTime), "moves/sec")

# Child processes have names: __mp_main__
if __name__ == "__main__": main()

#process = psutil.Process(os.getpid())
#mem = round(process.memory_info().rss / 1024 / 1024, 2)
#mem1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
#print("MEM1", round(mem, 2), "Mb")
