import chess
from evaluate import evaluate
import copy
from multiprocessing import Process, Queue, Value

# TODO Learn about castling properly!
# TODO Eliminate 3-fold repetition! See code of main.py
# TODO Implement time constraints to avoid "Black forfeits on time"

cores = 6         # How many CPU cores should we use?
count = 0         # Total count of nested calls within current ply
workers = []      # Workers stays in memory till the programm end
sharedAlpha = Value('i', -10000) # Sharing Alpha between Processes
future = [[], []] # Predicted best move trees for Black and White
bestTree = ""     # Store tree of next best moves to search it deeper then other moves
inq = Queue()     # Input moves queue for paraller workers
outq = Queue()    # Output results queue for paraller workers

def startWorkers():    
    workers = [ 
        Process(target = worker, args = (inq, outq, sharedAlpha))        
            for _ in range(cores)
    ]        
    for w in workers: w.start() # TODO 
    
def stopWorkers():
    for _ in range(cores): inq.put(None)    

def search(board: chess.Board, turn: bool, depth: int, maxDepth: int, alpha: int = -10000, beta: int = 10000):

    global count; count = 0        

    # Init global Alpha before starting pushing into queues
    with sharedAlpha.get_lock():
        sharedAlpha.value = -10000
    
    # Create queue of jobs for different workers
    moves  = list(board.legal_moves)
    for move in moves:        
        newBoard = copy.copy(board)
        newBoard.push(move)
        inq.put( (newBoard, turn, depth, alpha, beta, future[turn], {"maxDepth": maxDepth}) )

    bestMove = None
    bestScore = -10000
    bestTree = ""

    # Get all results
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

    ###print("\nTREE", bestTree)
    future[turn] = bestTree

    return bestMove, bestScore, count    

def negamax(board: chess.Board, turn: bool, depth: int, alpha: int, beta: int, tree = ""):

    # Lets count all nested calls for search within current move
    global count; count += 1  # TODO Mutex to avoid data races   

    # Just return evaluation for terminal nodes  
    # TODO Check for game_over ONLY if there None move was returned!  
    if depth == 0 or board.is_game_over():               
        return evaluate(board, turn), tree

    alphaTree = ""

    # Check all moves one by one
    for move in board.legal_moves:   

        board.push(move)  
        score, newTree = negamax(board, turn, depth-1, -beta, -alpha, tree + move.uci())            
        score = -score 
        board.pop() # TODO What if do not pop?

        if score > alpha:                         
            alpha = score            
            alphaTree = newTree
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
        # If there at least three moves in tree, 
        # we know the best next move from the previous iteration
        # and trying to dig into it with more depth
        if len(future) >= 12: # each moves tree coded like: f8b4c2c3f6e4
            if move.uci() == future[8:12]:                
                depth = maxDepth

        with sharedAlpha.get_lock():
            alpha = max(alpha, sharedAlpha.value)                                    

        score, tree = negamax(board, turn, depth-1, -beta, -alpha, move.uci())   
        score = -score 

        with sharedAlpha.get_lock():
            if score > sharedAlpha.value:
                sharedAlpha.value = score
                ##if score >= beta: # TODO Is it ever possible?
                ##    outq.put( (board.peek(), beta) )

        # Return bestMove and bestScore
        outq.put( (move, score, tree) )
