import chess
import random
from search import search
from log import log

# TODO Teach engine to play both white and black sides

def command(msg: str, board: chess.Board, depth: int):    
    """
    Accept UCI commands and respond.
    The board state is also updated.
    """

    #log(f">>> {msg}")

    if msg == "quit":
        log("\n[KAISSA64] Session was ended...")
        sys.exit()

    if msg == "uci":
        print("id name Kaissa64")  
        print("id author Serge Gotsuliak")
        print("uciok")
        return

    if msg == "isready":
        print("readyok")
        return

    if msg == "ucinewgame":
        # TODO ...
        return

    # Game started and we play whites
    if msg == "position startpos":
        board.clear()
        return

    # TODO Use chess.parse_uci()
    if "position startpos moves" in msg:
        moves = msg.split(" ")[3:]
        board.clear()
        board.set_fen(chess.STARTING_FEN)
        for move in moves:
            board.push(chess.Move.from_uci(move))
        return

    if "position fen" in msg:
        fen = " ".join(msg.split(" ")[2:])
        board.set_fen(fen)
        return

    if msg[0:2] == "go":
        #_move = next_move(depth, board)
        #moves = list(board.legal_moves)
        #move = random.choice(moves)
        score, move = search(board, depth, -100000, None)
        board.push(move)
        #print(f"bestmove {_move}")
        print(f"bestmove {move}")
        log(f"<<< bestmove {move}")
        return        