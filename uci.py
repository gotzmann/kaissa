import chess
import random
import sys
import argparse
from command import command
from log import log

defaultDepth = 1
board = chess.Board()

log("\n[KAISSA64] Start new session...")

while True:
    msg = input()
    print(f">>> {msg}", file=sys.stderr)
    command(msg, board, defaultDepth)

sys.exit()

#[KAISSA64] Start new session...
#>>> uci
#>>> ucinewgame
#>>> isready
#>>> position startpos moves e2e4
#>>> go wtime 180000 btime 180000 winc 2000 binc 2000
#<<< bestmove g8h6
#>>> position startpos moves e2e4
#>>> go wtime 180000 btime 180000 winc 2000 binc 2000
#<<< bestmove g8h6
#>>> quit
