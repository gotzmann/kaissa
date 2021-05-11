import chess
import random
import sys
import argparse
from command import command
from log import log
import time
from parallel import startWorkers, stopWorkers

#print("UCI NAME", __name__)

def main():    

    log("\n[KAISSA64] Start new session...\n")    
    start = time.time()    
    startWorkers() # Init multiprocessing           
    
    defaultDepth = 3
    if len(sys.argv) > 1:
        defaultDepth = int(sys.argv[1])

    board = chess.Board()    

    while True:
        msg = input()
        log(f">>> {msg}")    
        if msg == "quit": break
        command(msg, board, defaultDepth)

    stopWorkers()
    end = time.time()    
    log(f"\n[KAISSA64] Session was ended after {round(end - start, 2)} sec...")

# Child processes have names: __mp_main__
if __name__ == "__main__": main()


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