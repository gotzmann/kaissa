import chess
import random

# TODO 

def evaluate(board: chess.Board):

    score = random.randint(0, 10000)

    # loop over board squares
    # for (var square = 0; square < 128; square++) {

    # let piece = board[square]
          
    # make sure square contains a piece
    #    if (piece) {


    # calculate material score
    # score += pieceWeights[piece & 15];
            
    # calculate positional score
    # (piece & 8) ? (score += board[square + 8]) : (score -= board[square + 8]);

    #move = random.choice(moves)
    return score