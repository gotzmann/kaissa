import chess
import random
import sys
import argparse
#from movegeneration import next_move
from uci import uci

depth = 1
board = chess.Board()

while True:
    msg = input()
    print(f">>> {msg}", file=sys.stderr)
    uci(msg, board, depth)

sys.exit()

#######################################################

'''
max_moves = 10
move_count = max_moves

#while not board.is_checkmate():
while move_count >= max_moves:
    board = chess.Board()
    print("[", move_count, "]")
    for i in range(max_moves):
        if board.is_checkmate():
            move_count = i
            print("\n---------------")
            print(i + 1, "=>", move)
            print("---------------")    
            print(board)
            print("---------------")    
            print("!CHECK'N'МАТE!")
            print("---------------")
            break        
        moves = list(board.legal_moves)
        move = random.choice(moves)
        board.push(move)
        #print("\n---------------")
        #print(i, "=>", move)
        #print("---------------")    
        #print(board)
        #print("---------------")    
'''

