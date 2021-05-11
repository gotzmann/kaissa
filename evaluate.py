import chess
import random
import sys

# TODO Evaluate castling and mates properly
# TODO Do know about promotion!

# Relative values to evaluate the material score of the position

pieceWeights = {
    chess.PAWN:   100,
    chess.KNIGHT: 300,
    chess.BISHOP: 350,
    chess.ROOK:   500,
    chess.QUEEN:  900,
    chess.KING:   0,
}

positionWeights = [
#   a1  b1  c1  d1  e1  f1  g1  h1
#   ------------------------------
    0,  0,  5,  5,  0,  0,  5,  0, 
    5,  5,  0,  0,  0,  0,  5,  5,
    5, 10, 15, 20, 20, 15, 10,  5,
    5, 10, 20, 30, 30, 20, 10,  5,    
    5, 10, 20, 30, 30, 20, 10,  5,
    5, 10, 15, 20, 20, 15, 10,  5,
    5,  5,  0,  0,  0,  0,  5,  5,
    0,  0,  5,  5,  0,  0,  5,  0,
#   ------------------------------    
#   a8  b8  c8  d8  e8  f8  g8  h8
]    

# The core of the chess engine - evaluation function
# Calculate simple one using sum of material and positional scores

def evaluate(board: chess.Board, turn: bool):

    # TODO Mate in ply! Move to eval function as special heuristic?            
    if board.is_checkmate():
        #print("=== EVAL IN CHECK :", 10000 - board.ply(), "===")
        return 10000 - board.ply()                
    
    score = 0

    # The board already applied the move so we should use 
    # color of "previous" turn to evaluate score properly
    # turn = board.turn
    
    # Iterate over all 64 squares of board    
    for square in chess.SQUARES: 

        piece = board.piece_type_at(square)  # 1 .. 6 or None   

        if not piece: continue
            
        # Calculate material and positional score            
        if board.color_at(square) == chess.WHITE:
            score += pieceWeights[piece]
            score += positionWeights[square]                
        else:    
            score -= pieceWeights[piece]
            score -= positionWeights[square]

    if turn == chess.BLACK:
        score = -score
                    
    return score                        

def evaluateOK(board: chess.Board, turn: bool):

    # TODO Mate in ply! Move to eval function as special heuristic?            
    if board.is_checkmate():
        #print("=== EVAL IN CHECK :", 10000 - board.ply(), "===")
        return 10000 - board.ply()                
    
    score = 0

    # The board already applied the move so we should use 
    # color of "previous" turn to evaluate score properly
    # turn = board.turn
    
    # Iterate over all 64 squares of board    
    for square in chess.SQUARES: 

        piece = board.piece_type_at(square)  # 1 .. 6 or None   

        if not piece: continue
            
        # Calculate material and positional score            
        if board.color_at(square) == chess.WHITE:
            score += pieceWeights[piece]
            score += positionWeights[square]                
        else:    
            score -= pieceWeights[piece]
            score -= positionWeights[square]

    if turn == chess.BLACK:
        score = -score
                    
    return score                        
    