import chess
import random
from evaluate import evaluate
#import copy
#import os
#import psutil

count = 0

def search(board: chess.Board, turn: bool, depth: int, alpha: int = -10000, beta: int = 10000, returnMove: bool = False, returnCount: bool = False, tree: str = ""):

    # Lets count all nested calls for search within current move
    global count
    count = 0 if returnCount else count + 1    

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

#    oldAlpha = alpha
    #tempBestSourceSquare = None
    #tempBestTargetSquare = None
    
#    max = -10000
    bestMove = None
#    turn = board.turn

    for move in board.legal_moves:                

        # TODO Mate in ply! Move to eval function as special heuristic?        
        capturedPiece = board.piece_type_at(move.to_square)        
        if capturedPiece == chess.KING:
            return 10000 - board.ply()        
        #print("[ MOVE", move, "]")
            
        tree += " > " + move.uci()

        board.push(move)
        score = -search(board, not turn, depth-1, -beta, -alpha, tree = tree)
        board.pop()            
        
#        print("\n---------------")   
#        print(f"DEPTH {depth-1}", "WHITE" if board.turn else "BLACK", move, "=>", evaluate(board, turn))
#        print("---------------")   
#        print(board)
#        print("---------------")           

        if score > alpha: 

#            alpha = score
#            bestMove = move   


            if score >= beta: 
                #return beta
                if returnMove and returnCount:   
                    return beta, bestMove, count
                elif returnMove:
                    return beta, bestMove
                else:
                    return beta

            alpha = score
            bestMove = move   
                                  
#        if score > max: 
#            max = score
#            bestMove = move                        

            #if returnMove:
            #    print("\n---------------")                   
            #    print(f"MAX", "WHITE" if not board.turn else "BLACK", move, "=>", max)
            #    print("---------------")   
            #    print(board)
            #    print("---------------")   

        


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
    
#    if returnMove and returnCount:
#        return max, bestMove, count
#    elif returnMove:
#        return max, bestMove
#    else:    
#        return max
    #return max

    if returnMove and returnCount:
        return alpha, bestMove, count
    elif returnMove:
        return alpha, bestMove
    else:    
        return alpha



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
