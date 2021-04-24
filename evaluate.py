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

    #score = random.randint(0, 10000)
    score = 0

    # loop over board squares
    # for (var square = 0; square < 128; square++) {

    # Iterate over all 64 squares of board    
    for square in chess.SQUARES: 

        # let piece = board[square]          
        # make sure square contains a piece
        #    if (piece) {
        piece = board.piece_type_at(square)  # 1 .. 6 or None              
        #print(board.color_at(square))
        if piece:

            # calculate material score
            # score += pieceWeights[piece & 15];
             
            # and board.color_at(square) == chess.WHITE: # True for whites and False for blacks
            if board.color_at(square) == chess.WHITE:
                score += pieceWeights[piece]
                score += positionWeights[square]
            else:    
                score -= pieceWeights[piece]
                score -= positionWeights[square]
            
            # calculate positional score
            # (piece & 8) ? (score += board[square + 8]) : (score -= board[square + 8]);
            #print(chess.square_file(square))
            #print(square)
            #score += positionWeights[chess.square_file(square)]

            ###score += positionWeights[square]
    
    return score