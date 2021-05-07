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

    # TODO Current Player PoV !!!
    # https://www.researchgate.net/publication/262672371_A_Comparative_Study_of_Game_Tree_Searching_Methods
    # evaluate leaf gamePositionition from
    # current player’s standpoint


def evaluate(board: chess.Board, turn: bool):

#    print("\n************************************************************")
#    for square in chess.SQUARES:
#        print (square, chess.SQUARE_NAMES[square], positionWeights[square])
#    sys.exit()    
#    print("\n************************************************************")
    
    score = 0

    # The board already applied the move so we should use 
    # color of "previous" turn to evaluate score properly
    turn = ~board.turn
    
    # Iterate over all 64 squares of board    
    for square in chess.SQUARES: 

        piece = board.piece_type_at(square)  # 1 .. 6 or None   

        if not piece: continue
            
        # Calculate material and positional score            
        #if board.color_at(square) != board.turn:
#        if board.color_at(square) == chess.WHITE:
        if board.color_at(square) == turn:        
            score += pieceWeights[piece]
            score += positionWeights[square]                
        else:    
            score -= pieceWeights[piece]
            score -= positionWeights[square]

    #score = -score if turn == chess.BLACK else score
#    if turn == chess.BLACK:
#        score = -score
    
    #color = "WHITE" if turn == chess.WHITE else "BLACK"
    #print("\n-- EVAL", color, "-")
    #print(board)
    #print("---------------")
    #print("SCORE =>", score)   
                
    return score                        
    