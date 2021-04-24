import chess
import random

# TODO 

def search(board: chess.Board, depth: int, score: int):
    if depth == 0:
        score = evaluate(board)
        return score

    moves = board.legal_moves

    for move in moves:
        board.push(move)
        new_score = search(board, depth-1, score)
        board.pop()

        if new_score > score:
            best_move = move

    negamax( depth - 1)

    #move = random.choice(moves)
    #return random.randint(0, 10000)