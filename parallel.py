import chess
import random
from evaluate import evaluate
import copy
#import os
#import psutil
from multiprocessing import Pool, cpu_count
#from multiprocessing.pool import ThreadPool as Pool
import sys

# TODO Learn about castling properly!
# TODO Eliminate 3-fold repetition! See code of main.py
# TODO Implement time constraints to avoid "Black forfeits on time"

# Total count of nested calls within current ply
count: int = 0

#def search(board: chess.Board, turn: bool, depth: int, alpha: int = -10000, beta: int = 10000, returnMove: bool = False, returnCount: bool = False, tree: str = ""):
def search(board: chess.Board, turn: bool, depth: int, alpha: int = -10000, beta: int = 10000):

    global count; count = 0

  ####  doChess = True
    cores = 3
    #cores = cpu_count()
    print("CORES", cores)
    tasks = [[] for _ in range(cores)]
    results = []
    ###print(tasks)

    # Distribute all moves as tasks for different cores 
    core = 0
    for move in board.legal_moves:
        #newBoard = copy.copy(board)
        newBoard = copy.copy(board)
        newBoard.push(move)
        #result = pool.apply_async(negamax, args = (newBoard, depth-1, -beta, -alpha))    
        #results.append({ "move": move, "score": result })
        ###tasks[core].append( (newBoard, depth-1, -beta, -alpha) )
        #tasks[core].append( (newBoard, not turn, depth-1, -beta, -alpha) )
        tasks[core].append( (newBoard, turn, depth, alpha, beta) )
        #print(core)
        core = core + 1 if core < cores-1 else 0
        #print(core)

        #print(tasks)    

#    print(tasks)
#    sys.exit()   

    # Form [pool] of [tasks] for each core 
    # Each core will compute dozen moves in the [task] list one by one
    pool = Pool(cores)
    for task in tasks:   
        #for t in task:
        #    print(t[0]) 
        #result = pool.apply_async(negamax, args = (newBoard, depth-1, -beta, -alpha))  
        #result = pool.apply_async(map, args = (task))
        #print("=== TASK\n", task)
        result = pool.apply_async(map, [task])
        #result = pool.apply_async(mapping, [(1, 2, 3)])    
        results.append(result)

    pool.close()
    pool.join() 

    # Refresh Alpha/Beta depending on previous results
    ###for result in results:                
        ###a = result["score"].get()
        ###if a > alpha: 
           ### alpha = a
            ###print("NEW ALPHA", alpha)
        #if b > beta: beta = b

    bestMove = None
    bestScore = -10000

    # Results is the list of best moves from separate [task] lists
    # Lets choose the Best of the Bests move
    for result in results:            
        #score = -result["score"].get()
        ###score = -result["score"].get()
        #move, score = result.get()
        move, score = result.get()
        #print("BEST", move, score)
        #score = -score # !!!
        if score > bestScore:
            bestScore = score
            bestMove = move

    return bestMove, bestScore, count

 ####   while doChess:

        
#####        pool = Pool(6) # Use all available CPU cores
        
        #poolResults = []
        
 ####       total = 0
     ####   for move in moves:

         ####   pool = Pool(procs) # Use all available CPU cores

       ####     count = 0
           #### while count < procs and total < len(moves):                
               #### count += 1
            ####    total += 1

           ####     print(count, "OF", total)
                
               #### newBoard = copy.copy(board)
        ####        newBoard.push(move)
  ###              result = pool.apply_async(negamax, args = (newBoard, depth-1, -beta, -alpha))    
     ###           results.append({ "move": move, "score": result })

        ###    pool.close()
        ###    pool.join()

            # Refresh Alpha/Beta depending on previous results
      ###      for result in results:                
         ###       a = result["score"].get()
            ###    if a > alpha: 
               ###     alpha = a
                  ###  print("NEW ALPHA", alpha)
                #if b > beta: beta = b

 ###           if total >= len(moves):
    ###            doChess = False
                #break

###    bestMove = None
   ### bestScore = -10000
###    for result in results:            
        #score = -result["score"].get()
   ###     score = -result["score"].get()
      ###  if alpha > bestScore:
         ###   bestScore = score
            ###bestMove = result["move"]

    ###return bestMove, bestScore, count


#def search(board: chess.Board, turn: bool, depth: int, alpha: int = -10000, beta: int = 10000, returnMove: bool = False, returnCount: bool = False, tree: str = ""):
def searchOK(board: chess.Board, depth: int, alpha: int = -10000, beta: int = 10000):

    global count; count = 0
    
    pool = Pool() # Use all available CPU cores
    results = []

    for move in board.legal_moves:
        #newBoard = copy.copy(board)
        newBoard = copy.copy(board)
        newBoard.push(move)
        result = pool.apply_async(negamax, args = (newBoard, depth-1, -beta, -alpha))    
        results.append({ "move": move, "score": result })

    pool.close()
    pool.join()

    bestMove = None
    bestScore = -10000
    for result in results:            
        score = -result["score"].get()
        if score > bestScore:
            bestScore = score
            bestMove = result["move"]

    return bestMove, bestScore, count

#def negamax(board: chess.Board, depth: int, alpha: int, beta: int, tree: str = ""):             
def negamaxOK(board: chess.Board, depth: int, alpha: int, beta: int):

    # Lets count all nested calls for search within current move
    # TODO Mutex to avoid data races
    global count; count += 1    

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


def negamax(board: chess.Board, turn: bool, depth: int, alpha: int, beta: int):

    # Lets count all nested calls for search within current move
    # TODO Mutex to avoid data races
    global count; count += 1    

    # Just return evaluation for terminal nodes  
    # TODO Check for game_over ONLY if there None move was returned!  
    if depth == 0 or board.is_game_over():               
        return evaluate(board, turn)

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
        score = -negamax(board, not turn, depth-1, -beta, -alpha)      
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



#def negamax(board: chess.Board, depth: int, alpha: int, beta: int, tree: str = ""):             
#def negamax(board: chess.Board, depth: int, alpha: int, beta: int):
def map(tasks):
    #print("MAPPING", tasks)
    bestScore = -10000
    bestMove = None

    for task in tasks:

        #board: chess.Board, depth: int, alpha: int, beta: int
        board, turn, depth, alpha, beta = task
        score = -negamax(board, not turn, depth-1, -beta, -alpha)   
        #print(board.peek(), "=>", score)
        if score > bestScore:
            bestScore = score
            bestMove = board.peek()
            # TODO Change alpha / beta for next moves
 
    return bestMove, bestScore


