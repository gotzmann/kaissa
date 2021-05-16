import chess
from evaluate import evaluate
import copy
from multiprocessing import Process, Queue, Value

# TODO Learn about castling properly!
# TODO Eliminate 3-fold repetition! See code of main.py
# TODO Implement time constraints to avoid "Black forfeits on time"

# How many CPU cores should we use?
cores = 6

# Total count of nested calls within current ply
count = 0

# Workers stays in memory till the programm end
workers = []

# Sharing Alpha between Processes
sharedAlpha = Value('i', -10000)

# Predicted best move trees for Black and White
future = [[], []]

inq = Queue()
outq = Queue()

# Store tree of next best moves to search it deeper then other moves
bestTree = []

def startWorkers():    
    workers = [ 
        Process(target = worker, args = (inq, outq, sharedAlpha))        
            for _ in range(cores)
    ]        
    for w in workers: w.start() # TODO ??? w.Daemon = True
    
def stopWorkers():
    for _ in range(cores): inq.put(None)    

def search(board: chess.Board, turn: bool, depth: int, maxDepth: int, alpha: int = -10000, beta: int = 10000):

    global count; count = 0        

    # Init global Alpha before starting pushing into queues
    with sharedAlpha.get_lock():
        sharedAlpha.value = -10000
    
    # What was the last BEST move?
#    if board.ply() > 1:
 #       theBoard = copy.copy(board)
  #      theBoard.pop()
   #     wasBest = theBoard.pop().uci()
        #print("WAS BEST", wasBest)
#    else:
 #       wasBest = None    

    # Create queue of jobs for different workers
    moves  = list(board.legal_moves)
    for move in moves:        
        newBoard = copy.copy(board)
        newBoard.push(move)
        # Search previous best move deeper than others
#        if move.uci() == wasBest: 
            #print("WAS BEST", move, "+2")
 #           inq.put( (newBoard, turn, depth + 2, alpha, beta) )
  #      else:    
        inq.put( (newBoard, turn, depth, alpha, beta, future[turn], {"maxDepth": maxDepth}) )

    bestMove = None
    bestScore = -10000
    bestTree = []

    # Get all results
    # TODO Break by time-out and do more reliable processing here
    count = 0
    while True:        
        move, score, tree = outq.get()
        if score > bestScore:
            bestScore = score
            bestMove = move
            bestTree = tree
        count += 1    
        #print("===", move, "=>", score, " | BEST", bestMove)                
        if count == len(moves): break

#    seq = ""
#    for step in bestTree:
#        seq += " > " + step.uci()
#    print("\nTREE", seq)

    future[turn] = bestTree

    #print("FUTURE\n")
    #print(future)

    return bestMove, bestScore, count    

#def negamax(board: chess.Board, turn: bool, depth: int, alpha: int, beta: int, treeIn = []):
def negamax(board: chess.Board, turn: bool, depth: int, alpha: int, beta: int, tree = []):

    # Lets count all nested calls for search within current move
    # TODO Mutex to avoid data races
    global count; count += 1    



    ##tree = copy.deepcopy(tree)
    tree = copy.copy(tree)
    # Just return evaluation for terminal nodes  
    # TODO Check for game_over ONLY if there None move was returned!  
    if depth == 0 or board.is_game_over():               
        return evaluate(board, turn), tree

    """
    # We should get last move from the top of the board to compute check/mate situation correctly
    move = board.pop()

    # Heuristic to valuate the MATE move    
    if board.gives_check(move):            
        board.push(move)  
        if board.is_checkmate():      
            score = -(10000 - board.ply())
            print("TOP MATE", move, score)
            return score
        else:    
            board.pop()

    # Heuristic to valuate the CHECK move    
    if board.gives_check(move):            
        score = -(9000 - board.ply())        
        print("TOP CHECK", move, score)
        board.push(move)        
        return score

    # Return board to the initial state
    board.push(move)        
    """

    alphaTree = []

    # Check all moves one by one
    for move in board.legal_moves:   

        #tree = copy.deepcopy(tree)   

        #print("TREE 1\n", tree)
        #alphaTree = tree

        #if turn == board.turn:      
        tree.append(move)

        board.push(move)  
        ##print("TREE2\n", tree)
        #score, tree = -negamax(board, turn, depth-1, -beta, -alpha, tree)    
        score, newTree = negamax(board, turn, depth-1, -beta, -alpha, tree)            
        score = -score ### !!!
        ##print("TREE3\n", tree)
        
        
        board.pop() # TODO What if do not pop?

        #if turn == board.turn:      
        tree = tree[:-1]          

        if score > alpha:             
            # TODO Should look for order of later assignments and beta check
            alpha = score
            #tree.append(move)
            alphaTree = newTree

            # Print board for "root" moves
            #if returnMove:
            #    print("\n---------------")                   
            #    print(f"MAX", "WHITE" if board.turn else "BLACK", move, "=>", score)
            #    print("---------------")   
            #    board.push(move)
            #    print(board)
            #    board.pop()            
            #    print("---------------")   

            ##if score >= beta:             
            ##    return beta
                                          
    return alpha, alphaTree

def worker(inq: Queue, outq: Queue, sharedAlpha: Value):

    while True:

        args = inq.get()        
        if args is None: break # Stop worker    

        board, turn, depth, alpha, beta, future, options = args
        move = board.peek()

        maxDepth = options.get("maxDepth", depth)
        if len(future) > 1:
            #print(move, "==", future[2])
            if move == future[2]:                
                #depth += 2 # TODO Make special parameter!
                depth = maxDepth
                #print(move, "==", future[2], "=>", depth)

        with sharedAlpha.get_lock():
            alpha = max(alpha, sharedAlpha.value)                                    

        #score, tree = -negamax(board, turn, depth-1, -beta, -alpha)   
        score, tree = negamax(board, turn, depth-1, -beta, -alpha, [move])   
        score = -score ### !!!

        #print("WORKER TREE\n", tree)

        with sharedAlpha.get_lock():
            if score > sharedAlpha.value:
                sharedAlpha.value = score
                ##if score >= beta: # TODO Is it ever possible?
                ##    outq.put( (board.peek(), beta) )

        #print(board.peek(), "=>", score, " | ", alpha, " .. ", beta)

        # Return bestMove and bestScore
        outq.put( (move, score, tree) )
