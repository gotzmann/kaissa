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
        return evaluate(board, turn)

    bestMove = None

    for move in board.legal_moves:                

        # TODO Mate in ply! Move to eval function as special heuristic?        
        capturedPiece = board.piece_type_at(move.to_square)        
        if capturedPiece == chess.KING:
            return 10000 - board.ply()                
            
        tree += " > " + move.uci()

        board.push(move)
        score = -search(board, not turn, depth-1, -beta, -alpha, tree = tree)
        board.pop()            
        
        if score > alpha: 

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
                                  
            #if returnMove:
            #    print("\n---------------")                   
            #    print(f"MAX", "WHITE" if not board.turn else "BLACK", move, "=>", alpha)
            #    print("---------------")   
            #    print(board)
            #    print("---------------")   
        
    if returnMove and returnCount:
        return alpha, bestMove, count
    elif returnMove:
        return alpha, bestMove
    else:    
        return alpha
