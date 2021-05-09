import chess
import random
from evaluate import evaluate
#import copy
#import os
#import psutil

count = 0

# TODO Learn about castling properly!

def search(board: chess.Board, turn: bool, depth: int, alpha: int = -10000, beta: int = 10000, returnMove: bool = False, returnCount: bool = False, tree: str = ""):

    # Lets count all nested calls for search within current move
    global count
    count = 0 if returnCount else count + 1    

    # Just return evaluation for terminal nodes    
    if depth == 0 or board.is_game_over():               
        return evaluate(board, turn)

    bestMove = None

    for move in board.legal_moves:                

        # TODO Mate in ply! Move to eval function as special heuristic?        
#        capturedPiece = board.piece_type_at(move.to_square)        
#        if capturedPiece == chess.KING:
#            return 10000 - board.ply()                
            
        tree += " > " + move.uci()

        board.push(move)
        score = -search(board, not turn, depth-1, -beta, -alpha, tree = tree)
        board.pop()            
        
        if score > alpha: 

            # TODO Should look for order of later assignments and beta check
            alpha = score
            bestMove = move   

            # Print board for "root" moves
            if returnMove:
                print("\n---------------")                   
                print(f"MAX", "WHITE" if board.turn else "BLACK", move, "=>", score)
                print("---------------")   
                board.push(move)
                print(board)
                board.pop()            
                print("---------------")   

            if score >= beta: 
            #    print ("BETA |", beta, "- DEPTH |", depth-1)                
                if returnMove and returnCount:   
                    return beta, bestMove, count
                elif returnMove:
                    return beta, bestMove
                else:
                    return beta
                                          
    if returnMove and returnCount:
        return alpha, bestMove, count
    elif returnMove:
        return alpha, bestMove
    else:    
        return alpha
