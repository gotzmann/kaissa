import chess
import random
import sys

# TODO Evaluate board both for blacks and whites

# Relative values to evaluate the material score of the position

pieceWeights = {
    chess.PAWN:   100,
    chess.KNIGHT: 300,
    chess.BISHOP: 350,
    chess.ROOK:   500,
    chess.QUEEN:  900,
    chess.KING:   0,
}

# TODO Do we need to mirror list of positions vertically?

positionWeights = [
    0,  0,  5,  5,  0,  0,  5,  0, 
    5,  5,  0,  0,  0,  0,  5,  5,
    5, 10, 15, 20, 20, 15, 10,  5,
    5, 10, 20, 30, 30, 20, 10,  5,    
    5, 10, 20, 30, 30, 20, 10,  5,
    5, 10, 15, 20, 20, 15, 10,  5,
    5,  5,  0,  0,  0,  0,  5,  5,
    0,  0,  5,  5,  0,  0,  5,  0,
]    

# The core of the chess engine - evaluation function
# Calculate simple one using sum of material and positional scores

def evaluate(board: chess.Board):
    
    score = 0

    # The board already applied the move so we should use 
    # color of "previous" turn to evaluate score properly
    turn = not board.turn
    
    # Iterate over all 64 squares of board    
    for square in chess.SQUARES: 

        piece = board.piece_type_at(square)  # 1 .. 6 or None                      
        if piece:
            
            # Calculate material and positional score            
            #if board.color_at(square) != board.turn:
            if board.color_at(square) == chess.WHITE:
            #if board.color_at(square) == turn:
                score += pieceWeights[piece]
                score += positionWeights[square]                
            else:    
                score -= pieceWeights[piece]
                score -= positionWeights[square]

    #score = -score if turn == chess.BLACK else score
    if turn == chess.BLACK:
        score = -score
    
    #color = "WHITE" if turn == chess.WHITE else "BLACK"
    #print("\n-- EVAL", color, "-")
    #print(board)
    #print("---------------")
    #print("SCORE =>", score)   
                
    return score                        
    