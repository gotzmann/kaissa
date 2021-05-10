import chess
import random
from evaluate import evaluate
import copy
#import os
#import psutil
from multiprocessing import Pool
import sys

count = 0

# TODO Learn about castling properly!
# TODO Eliminate 3-fold repetition! See code of main.py
# TODO Implement time constraints to avoid "Black forfeits on time"

def choose(result):
    print("=== CHOOSE ===")
    print(result)
    print("=== \CHOOSE ===")

def search(board: chess.Board, turn: bool, depth: int, alpha: int = -10000, beta: int = 10000, returnMove: bool = False, returnCount: bool = False, tree: str = ""):
    
    print ("SEARCH", __name__)
    # Lets parallel execution of search
    #if __name__ == '__main__':        
    if returnMove:                 
        pool = Pool(1)
        results = []
        try:       
            #pool = Pool(len(moves))            
            #with Pool(len(moves)) as pool:        
            for move in board.legal_moves:   
                print(move) 
                newBoard = copy.deepcopy(board)
                newBoard.push(move)
    #            pool.apply_async(negamax, args = (newBoard, depth-1, -beta, -alpha), callback = choose) 
                args = (newBoard, depth-1, -beta, -alpha)
                results.append({ 
                    "move": move.uci(), 
                    "result": pool.apply_async(negamax, args, choose),
                }) 
#                print(result.get())
#                print("RESULT", result)
                #answer = sum(p.map(if_prime, list(range(1000000))))  
                #score = -search(board, not turn, depth-1, -beta, -alpha, tree = tree)      
    #        pool.close()    
    #        pool.join()    
            #sys.exit()        
            for result in results:
                result["result"].wait()
        finally:
            print("FINALLY")
            print(results)
#            for result in results:
 #               move, score = result
            #pool.terminate()
            #pool.join()    

    pool.join()    
    sys.exit()

#pool = mp.Pool()
#    for i in range(10):
 #       pool.apply_async(foo_pool, args = (i, ), callback = log_result)
  #  pool.close()
   # pool.join()
    #print(result_list)                

    # Lets count all nested calls for search within current move
    global count
    count = 0 if returnCount else count + 1    

    # Just return evaluation for terminal nodes  
    # TODO Check for game_over ONLY if there None move was returned!  
    if depth == 0 or board.is_game_over():               
        return evaluate(board, turn)

    bestMove = None

    for move in board.legal_moves:      
        
        board.push(move)        
        treeBefore = tree
        tree += move.uci() + " > "         

        # We should see immediate checks
        if board.is_checkmate():            
            score = 10000 - board.ply()
        else:                
            score = -search(board, not turn, depth-1, -beta, -alpha, tree = tree)
        tree = treeBefore            
        board.pop()                            

        if score > alpha:             
            # TODO Should look for order of later assignments and beta check
            alpha = score
            bestMove = move   

            # Print board for "root" moves
            #if returnMove:
            #    print("\n---------------")                   
            #    print(f"MAX", "WHITE" if board.turn else "BLACK", move, "=>", score)
            #    print("---------------")   
            #    board.push(move)
            #    print(board)
            #    board.pop()            
            #    print("---------------")   

            if score >= beta:             
                if returnMove and returnCount:   
                    return beta, bestMove, count
                elif returnMove:
                    return beta, bestMove
                else:
                    return beta
                                          
    if returnMove and returnCount:
        return alpha, bestMove, count
    elif returnMove:
        return alpha, bestMove
    else:    
        return alpha

def negamax(board: chess.Board, depth: int, alpha: int, beta: int, tree: str = ""):             

    print("NEGAMAX")
    return 666

    # Lets count all nested calls for search within current move
    #global count
    #count = 0 if returnCount else count + 1    

    # Just return evaluation for terminal nodes  
    # TODO Check for game_over ONLY if there None move was returned!  
    if depth == 0 or board.is_game_over():               
        return evaluate(board, board.turn)

    bestMove = None

    for move in board.legal_moves:      
        
        board.push(move)        
#        treeBefore = tree
#        tree += move.uci() + " > "         

        # We should see immediate checks
#        if board.is_checkmate():            
#            score = 10000 - board.ply()
#        else:                
#            score = -search(board, not turn, depth-1, -beta, -alpha, tree = tree)
#        tree = treeBefore      
        score = -negamax(board, depth-1, -beta, -alpha)      
        board.pop()                            

        if score > alpha:             
            # TODO Should look for order of later assignments and beta check
            alpha = score
            bestMove = move   

            # Print board for "root" moves
            #if returnMove:
            #    print("\n---------------")                   
            #    print(f"MAX", "WHITE" if board.turn else "BLACK", move, "=>", score)
            #    print("---------------")   
            #    board.push(move)
            #    print(board)
            #    board.pop()            
            #    print("---------------")   

            if score >= beta:             
                return beta
                                          
    return alpha
