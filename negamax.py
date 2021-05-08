import chess
import random
from evaluate import evaluate
#import copy
#import os
#import psutil

count = 0
#best_move = chess.Move.from_uci("a2a3")
#best_move = None
#temp_move = None

#bestMove = None

#def negamax(board: chess.Board, depth: int, max: int):
def search(board: chess.Board, turn: bool, depth: int, alpha: int = -10000, beta: int = 10000, returnMove: bool = False, returnCount: bool = False, tree: str = ""):

    # Lets count all nested calls for search within current move
    global count
    count = 0 if returnCount else count + 1    
    #tempBestMove = None
    
    #global best_move, temp_move

    #global count
    #count += 1

    # TODO Current Player PoV !!!
    # https://www.researchgate.net/publication/262672371_A_Comparative_Study_of_Game_Tree_Searching_Methods
    # evaluate leaf gamePositionition from
    # current player’s standpoint
    #if depth == 0 or gameIsOver???:               
    if depth == 0:               

#        print("\n---------------") 
#        print(tree, "=>", evaluate(board, turn))  
#        print("---------------")   
        #print(f"TERMINAL", "WHITE" if turn else "BLACK", "=>", evaluate(board, turn))
        #print("---------------")   
#        print(board)
#        print("---------------")   

        return evaluate(board, turn)

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

#    oldAlpha = alpha
    #tempBestSourceSquare = None
    #tempBestTargetSquare = None
    
    max = -10000
    bestMove = None
#    turn = board.turn

    for move in board.legal_moves:                

        # TODO Mate in ply! Move to eval function as special heuristic?        
        capturedPiece = board.piece_type_at(move.to_square)        
        if capturedPiece == chess.KING:
            return 10000 - board.ply()        

        board.push(move)
        #new_score, new_move = search(board, depth-1, best_score, best_move)        
        #new_score, new_move = search(board, depth-1, -10000, best_move)        
        #new_score = -new_score
                      
        #// return mating score if king has been captured
        #if((capturedPiece & 7) == 3) return 10000 - ply; // mate in "ply"

        #score, _ = search(copy.deepcopy(board), depth-1, max)        
        #score = negamax(copy.deepcopy(board), depth-1, max)
        #score = negamax(board, depth-1, max)

        #score = -search(board, depth-1, -beta, -alpha)
        
        # https://github.com/aaron-hanson/negamax-alpha-beta/blob/master/index.js

        #sideChanged = 1 if board.turn == turn else -1
        # Do not inverse score for the first search where moving side stays same
#        if returnMove:
#            sideChanged = 1
#        else:    
#            sideChanged = -1

#        score = sideChanged * search(
#            board, 
#            turn,
#            depth-1, 
#            sideChanged * alpha, 
#            sideChanged * beta
#        )

        tree += " > " + move.uci()
        #score = sideChanged * search(board, turn, depth-1, -beta, -alpha, tree = tree)
        #score = -search(board, turn, depth-1, -beta, -alpha, tree = tree)
        #score = sideChanged * search(board, turn, depth-1, sideChanged * alpha, sideChanged * beta, tree = tree)
        #score = -search(board, turn, depth-1, -beta, -alpha, tree = tree)
#        score = sideChanged * search(board, turn, depth-1, -beta, -alpha, tree = tree)
        score = -search(board, not turn, depth-1, -beta, -alpha, tree = tree)
        
#        print("\n---------------")   
#        print(f"DEPTH {depth-1}", "WHITE" if board.turn else "BLACK", move, "=>", evaluate(board, turn))
#        print("---------------")   
#        print(board)
#        print("---------------")           

        #bestMove = move

        if score > max: 
            max = score
            bestMove = move            
            #tempBestMove = move

            if returnMove:
                print("\n---------------")   
                print(f"MAX", "WHITE" if not board.turn else "BLACK", move, "=>", evaluate(board, turn))
                print("---------------")   
                print(board)
                print("---------------")   

        board.pop()            


        # adjust the search window
        #if score > alpha:
####        if max > alpha: 
####            alpha = max
#            bestMove = move
            #if score >= beta: return beta                
            #tempBestMove = move

        # cut off
####        if alpha >= beta: 
####            break
            #return beta                    
 #           return alpha

        #if max >= beta: 
        #    break
        
#    if alpha != oldAlpha:
#       bestMove = tempBestMove
    
    if returnMove and returnCount:
        return max, bestMove, count
    elif returnMove:
        return max, bestMove
    else:    
        return max
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
