import chess
import random

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