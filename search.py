import chess
import random
from evaluate import evaluate

#best_move = None
def search(board: chess.Board, depth: int, best_score: int, best_move: chess.Move):

    if depth == 0:
        score = evaluate(board)      
        return score, None

    moves = board.legal_moves

    for move in moves:
        board.push(move)
        #new_score, new_move = search(board, depth-1, best_score, best_move)        
        #new_score, new_move = search(board, depth-1, -10000, best_move)        
        #new_score = -new_score

        new_score, new_move = search(board, depth-1, best_score, best_move)        
        #new_score = -new_score

        if new_score > best_score:
            best_score = new_score
            best_move = move
            
            #print("\n-- BEST MOVE --")
            #print(board)
            #print("---------------")            
            #print("MAX =>", best_score, "|", best_move)

        board.pop()    

    return best_score, best_move
