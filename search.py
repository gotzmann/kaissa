import chess
import random
from evaluate import evaluate

best_move = None
def search(board: chess.Board, depth: int, score: int):

    if depth == 0:
        score = evaluate(board)
        #print("\n--- SEARCH! ---")
        #print(board)
        #print("---------------")
        #print("SCORE =>", score)
        return score

    moves = board.legal_moves

    for move in moves:
        board.push(move)
        new_score = search(board, depth-1, score)
        board.pop()

        if new_score > score:
            score = new_score
            best_move = move
            #print("[MAX] =>", score, "|", move)

    return best_move
