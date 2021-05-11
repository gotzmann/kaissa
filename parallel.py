import chess
from evaluate import evaluate
import copy
from multiprocessing import Process, Queue

# TODO Learn about castling properly!
# TODO Eliminate 3-fold repetition! See code of main.py
# TODO Implement time constraints to avoid "Black forfeits on time"

# How many CPU cores should we use?
cores: int = 4

# Total count of nested calls within current ply
count: int = 0

# Workers stays in memory till the programm end
workers = []

inq = Queue()
outq = Queue()

def startWorkers():
    #print("WORKERS")
    workers = [ 
        Process(target = worker, args = (inq, outq))
            for _ in range(cores)
    ]
    #print("START")
    for w in workers: 
        #w.Daemon = True
        w.start()
    
def stopWorkers():
    for _ in range(cores): inq.put(None)

#def search(board: chess.Board, turn: bool, depth: int, alpha: int = -10000, beta: int = 10000, returnMove: bool = False, returnCount: bool = False, tree: str = ""):
def search(board: chess.Board, turn: bool, depth: int, alpha: int = -10000, beta: int = 10000):

    global count; count = 0

 ###   inq = Queue()
 ###   outq = Queue()

  ####  doChess = True

    #cores = cpu_count()
    #print("CORES", cores)
###    tasks = [[] for _ in range(cores)]
    results = []
    ###print(tasks)

    # Distribute all moves as tasks for different cores 
    #####core = 0
    moves  = list(board.legal_moves)
    for move in moves:
        #newBoard = copy.copy(board)
        newBoard = copy.copy(board)
        newBoard.push(move)
        #result = pool.apply_async(negamax, args = (newBoard, depth-1, -beta, -alpha))    
        #results.append({ "move": move, "score": result })
        ###tasks[core].append( (newBoard, depth-1, -beta, -alpha) )
        #tasks[core].append( (newBoard, not turn, depth-1, -beta, -alpha) )

        #####tasks[core].append( (newBoard, turn, depth, alpha, beta) )
        #q.put( (newBoard, turn, depth, alpha, beta) )

        inq.put( (newBoard, turn, depth, alpha, beta) )
        #print(core)
        #####core = core + 1 if core < cores-1 else 0
        #print(core)
        #print(tasks)    

    #return     
    # Stop signals for each process
###    for _ in range(cores): inq.put(None)
    #print("JOIN")
    # Wait while boards are processing
#############################################    for w in workers: w.join()

    # Stop all workers
###    for _ in range(cores): inq.put(None)

    bestMove = None
    bestScore = -10000

    # Get all results
    count = 0
    while True:
        ##########################################################result = outq.get()
        #print("INSIDE LOOP")
        move, score = outq.get() ######################################## result
        ##################################################print(move, "=>", score)
        # TODO Break by time-out and do more reliable processing here
        #################################################results.append(result)
        if score > bestScore:
            bestScore = score
            bestMove = move
        count += 1    
        if count == len(moves): break

    # Results is the list of best moves from separate [task] lists
    # Lets choose the Best of the Bests move
    ###########################################################for result in results:            
        #score = -result["score"].get()
        ###score = -result["score"].get()
        #move, score = result.get()
        ############################################################move, score = result
        #print("BEST", move, score)
        #score = -score # !!!
    ####################################################    if score > bestScore:
     #######################################################       bestScore = score
     ############################################################       bestMove = move

    return bestMove, bestScore, count    

    return    
    
    # Starting jobs with ALL processes
    for task in tasks:
        print("PROCESS")
        p = Process(target=map, args=[task])
        p.Daemon = True
        p.start()

    # Awaiting while ALL tasks end up execution    
    for task in tasks:
        p.join()
    #print time.time()-t
    #while True:
        #print q.get()    


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

def negamax(board: chess.Board, turn: bool, depth: int, alpha: int, beta: int):

    #print("============")
    #print(board)

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


def worker(inq: Queue, outq: Queue):

    while True:
        args = inq.get()
        #print("WORKER")
        #print(args)

        # Stop worker
        #if args is None: print("LEAVE WORKER"); break
        if args is None: break

#        bestScore = -10000
#        bestMove = None

#    for task in tasks:

        #board: chess.Board, depth: int, alpha: int, beta: int
        board, turn, depth, alpha, beta = args
        score = -negamax(board, not turn, depth-1, -beta, -alpha)   
        #print(board.peek(), "=>", score)
        #if score > bestScore:
        #    bestScore = score
        #    bestMove = board.peek()
            # TODO Change alpha / beta for next moves
 
        #return bestMove, bestScore

        outq.put( (board.peek(), score) )
