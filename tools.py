import chess
import copy

boards = [] 

def printBoard():

    # Print board for "root" moves
    #if returnMove:
    #    print("\n---------------")                   
    #    print(f"MAX", "WHITE" if board.turn else "BLACK", move, "=>", score)
    #    print("---------------")   
    #    board.push(move)
    #    print(board)
    #    board.pop()            
    #    print("---------------")   



def check3Fold(board):        

    # Check for 3-fold rule
    # TODO Store hash of FEN strings to speed up things
    boards.append(copy.copy(board))

    if len(boards) > 8:

        folds = 1
        # Traverse over all previous board states from the one 
        # before the current and calculate repetitions
        for b in boards[-2:-10:-1]:
            if board.board_fen() == b.board_fen():
                folds += 1

        if folds == 3:
            print("===============")
            print("    3-FOLD!    ")        
            print("===============")
            return True
            
    return False


