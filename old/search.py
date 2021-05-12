import chess
import random
from evaluate import evaluate
import copy
import os
import psutil

#count = 0
#best_move = chess.Move.from_uci("a2a3")
#best_move = None
#temp_move = None

bestMove = None

#def negamax(board: chess.Board, depth: int, max: int):
def negamax(board: chess.Board, depth: int, alpha: int, beta: int):
    global bestMove
    tempBestMove = None
    
    #global best_move, temp_move

    #global count
    #count += 1

    #if depth == 0 or gameIsOver???:               
    if depth == 0:               
        #return evaluate(board), None
        return evaluate(board)

    #max = -10000 # -Infinity
    #best_move = None        
    #process = psutil.Process(os.getpid())
    #mem = round(process.memory_info().rss / 1024 / 1024, 1)
    #mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    #print(f"--[ {depth} ] | # {count} | {mem} Mb ------------------------------------------")
    #print(f"--[ {depth} ] | {mem} Mb ------------------------------------------")
    #print("MEM", mem, "Mb")
    #print("TOTAL LEGAL MOVES:", len(list(board.legal_moves)))
    #print([move.uci() for move in board.legal_moves], "=>", len(list(board.legal_moves)))

    oldAlpha = alpha
    #tempBestSourceSquare = None
    #tempBestTargetSquare = None
    tempBestMove = None
    max = -10000

    for move in board.legal_moves:                

        # if ((capturedPiece & 7) == 3) return 10000 - ply; // mate in "ply"
#        capturedPiece = board.piece_type_at(move.to_square)
        #color = board.color_at(square)
#        if capturedPiece == chess.KING:
#            return 10000

        #print(move, " | ", evaluate(board))

        board.push(move)
        #new_score, new_move = search(board, depth-1, best_score, best_move)        
        #new_score, new_move = search(board, depth-1, -10000, best_move)        
        #new_score = -new_score
                      
        #// return mating score if king has been captured
        #if((capturedPiece & 7) == 3) return 10000 - ply; // mate in "ply"

        #score, _ = search(copy.deepcopy(board), depth-1, max)        
        #score = negamax(copy.deepcopy(board), depth-1, max)
        #score = negamax(board, depth-1, max)

        score = -negamax(board, depth-1, -beta, -alpha)

        
        #board_copy = copy.deepcopy(board)
        #board_copy.push(move)            
        #print("\n-- BEST MOVE --")
        print(f"\n[ {depth} ]", "WHITE" if not board.turn else "BLACK", move, "=>", evaluate(board))
        print("---------------")   
        print(board)
        print("---------------")   

        board.pop()    

        #bestMove = move

        if score > max: 
            max = score
            #bestMove = move
            tempBestMove = move

        #if score > alpha:
        if max > alpha: 
            alpha = max
            #if score >= beta: return beta                
            #tempBestMove = move

#        if alpha >= beta: 
            #return beta                    
 #           return alpha

        if max >= beta: 
            break
        
    if alpha != oldAlpha:
       bestMove = tempBestMove
    
    return alpha
    #return max


#        print(depth, "|", "WHITE" if not board.turn else "BLACK", "|", move, "|", score)

        #if new_score > best_score:
#        if score > max:
            #best_score = new_score
#            max = score
#            best_move = move
            #temp_move = move
            
            #print(depth, "|", "WHITE" if not board.turn else "BLACK", "|", move, "|", score)
            #board_copy = copy.deepcopy(board)
            #board_copy.push(move)            
            #print("\n-- BEST MOVE --")
            #print(board_copy)
            #print("---------------")                                

    #return best_score, best_move
    #return max, best_move

    #best_move = temp_move
    #print("SEARCH", temp_move, best_move)

#    return max
