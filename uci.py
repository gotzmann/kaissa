import chess
import random
import sys
import argparse
from command import command
from log import log
import time

start = time.time()

defaultDepth = 5
board = chess.Board()

log("\n[KAISSA64] Start new session...\n")

while True:
    msg = input()
    log(f">>> {msg}")    
    command(msg, board, defaultDepth)

end = time.time()
log("\nTIME", round(end - start, 2), "sec")

log("\n[KAISSA64] Session was ended...")

sys.exit()

# --- Python Simple Chess Log ---

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

# --- Arena Log ---

#>>> xboard
#>>> uci
#>>> isready
#>>> ucinewgame
#>>> isready
#>>> position startpos
#... clear board
#>>> go wtime 300000 btime 300000 winc 0 binc 0
#... searching with depth 1
#... push move None => -10000