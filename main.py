import chess
from parallel import search, startWorkers, stopWorkers
import sys
import time
import copy
import math

# TODO Compute count correctly
# TODO Save best computed moves for later? I mean cache the game tree

# TODO Compute Moves Per Second metric to understand the average performance
# TODO no castling
# TODO no enpassant
# TODO no 3 fold repetition
# TODO no 50 rule move count

# TODO Check what's wrong with the 4/6 depth not seening the mate?
#      [White "02"][Black "46"][Result "1-0"] 
#      1. e4 Nc6 2. Bd3 Ne5 3. Bb5 c6 4. Ba4 b5 
#      5. Bb3 g5 6. d4 Nc4 7. Bxg5 Nxb2 8. Qf3 h6 9. Qxf7# 1-0

def main():        

    startWorkers() # Init multiprocessing

    start = time.time()

    maxPlies = 6 # 0 for unlimited moves    
    if len(sys.argv) > 1:
        depth = int(sys.argv[1])
        if depth < 10: # for example: 3 both for default and max depth
            defaultDepth = depth
            maxDepth = defaultDepth
        else: # 37 for example: 3 for default and 7 for max depth               
            defaultDepth = math.floor(depth / 10)
            maxDepth = depth % 10
    else:    
        defaultDepth = 3    
        maxDepth = defaultDepth
    #print(depth, defaultDepth, maxDepth)
    #sys.exit()
    movesPerSecond = 0
    board = chess.Board()
    boards = [] # we should check for 3-fold repetition and similar things

#    board.push(chess.Move.from_uci("e2e4"))
#    board.push(chess.Move.from_uci("e7e5"))
#    board.push(chess.Move.from_uci("g1f3"))    

    print("\n===============")    
    print("     START     ")
    print("===============")    
    print(board)
    print("===============")        
        
    while not maxPlies or board.ply() < maxPlies:

        print("\n[", len(list(board.legal_moves)), "] =>", [ move.uci() for move in board.legal_moves ])

        move, score, count = search(board, board.turn, defaultDepth, maxDepth)    

        board.push(move)   
        movesPerSecond += count

        print("\n===============")    
        print(f"MOVE {board.ply()} => {move} of {count} => {score}")
        print("===============")    
        print(board)
        print("===============")        

        # Check for 3-fold rule
        # TODO Store hash of FEN strings to speed up things
        boards.append(copy.copy(board))
        if len(boards) > 8:
            folds = 1
            # Traverse over all previous board states from the one 
            # before the current and calculate repetitions
            for b in boards[-2:-10:-1]:
                if board.board_fen() == b.board_fen():
                    folds += 1

            if folds == 3:
                print("===============")
                print("    3-FOLD!    ")        
                print("===============")
                break

        if board.is_game_over():
            print("===============")
            print("   GAME OVER   ")
            print("     ", board.outcome().result())        
            print("===============")
            break        
    
    end = time.time()
    execTime = end - start

    stopWorkers()

    print("\n[TIME]", round(execTime, 2), "sec")
    print("[MPS]", round(movesPerSecond / execTime), "moves/sec")

# Child processes have names: __mp_main__
if __name__ == "__main__": main()
