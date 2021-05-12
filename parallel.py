import chess
from evaluate import evaluate
import copy
from multiprocessing import Process, Queue

# TODO Learn about castling properly!
# TODO Eliminate 3-fold repetition! See code of main.py
# TODO Implement time constraints to avoid "Black forfeits on time"

# How many CPU cores should we use?
cores = 6

# Total count of nested calls within current ply
count = 0

# Workers stays in memory till the programm end
workers = []

inq = Queue()
outq = Queue()

def startWorkers():    
    workers = [ 
        Process(target = worker, args = (inq, outq))        
            for _ in range(cores)
    ]        
    for w in workers: w.start() # TODO ??? w.Daemon = True
    
def stopWorkers():
    for _ in range(cores): inq.put(None)    

def search(board: chess.Board, turn: bool, depth: int, alpha: int = -10000, beta: int = 10000):

    global count; count = 0

    #cores = cpu_count()
    results = []    

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

        #####core = core + 1 if core < cores-1 else 0


    bestMove = None
    bestScore = -10000

    # Get all results
    count = 0
    while True:
        ##########################################################result = outq.get()
        
        move, score = outq.get() ######################################## result
        #print(move, "=>", score)        
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
        
        #score = -score # !!!
    ####################################################    if score > bestScore:
     #######################################################       bestScore = score
     ############################################################       bestMove = move

    return bestMove, bestScore, count    

def negamax(board: chess.Board, turn: bool, depth: int, alpha: int, beta: int):

    # Lets count all nested calls for search within current move
    # TODO Mutex to avoid data races
    global count; count += 1    

    # Just return evaluation for terminal nodes  
    # TODO Check for game_over ONLY if there None move was returned!  
    if depth == 0 or board.is_game_over():               
        return evaluate(board, turn)

#######################################################################    bestMove = None
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
    # Check all moves one by one
    for move in board.legal_moves:      
    
        board.push(move)        
#        treeBefore = tree
#        tree += move.uci() + " > "         

        # We should see immediate checks
        #print(move, "=> board_check?")
#        if board.is_checkmate():            
#            score = 10000 - board.ply()                
#            print("CHECKMATE INSIDE", move, score)
            # TODO Whats the right sign here?            
            #if turn == chess.BLACK:
##            if turn == board.turn:
##                score = -score  
        # TODO Move other fugures close to checking king 
        #      Calculate some form of distance here?
#        elif board.is_check():            
#            score = 9000 - board.ply()                
#            print("CHECK INSIDE", move, score)
            # TODO Whats the right sign here?            
            #if turn == chess.BLACK:
##            if turn == board.turn:
##                score = -score            
#        else:                
#            score = -negamax(board, not turn, depth-1, -beta, -alpha)      
#        tree = treeBefore 
      
        ###score = -negamax(board, not turn, depth-1, -beta, -alpha)      
        score = -negamax(board, turn, depth-1, -beta, -alpha)      

        # TODO What if do not pop?
        board.pop()                            

        if score > alpha:             
            # TODO Should look for order of later assignments and beta check
            alpha = score
#################################################################################            bestMove = move   

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

def worker1(inq: Queue, outq: Queue):

    while True:

        args = inq.get()
        if args is None: break

        board, turn, depth, alpha, beta = args
        score = -negamax(board, not turn, depth-1, -beta, -alpha)   

        # Return bestMove and bestScore
        outq.put( (board.peek(), score) )

def worker(inq: Queue, outq: Queue):

    # We must init all params on the very first move 
    ply = -1

    while True:
        args = inq.get()

        # Stop worker        
        if args is None: break

        #board: chess.Board, depth: int, alpha: int, beta: int
        board, turn, depth, a, b = args
        #board, turn, depth, alpha, beta = args

        # Init all params with defaults on every new move
        if board.ply() != ply:
            ply = board.ply()
            alpha = a
            beta = b                       

        ###score = -negamax(board, not turn, depth-1, -beta, -alpha)   
        score = -negamax(board, turn, depth-1, -beta, -alpha)   

        #print("#", ply, board.peek(), "=>", score, " | ", alpha, " .. ", beta)
        if score > alpha:
            alpha = score
            if score >= beta: # TODO Is it ever possible?
                outq.put( (board.peek(), beta) )

        # Return bestMove and bestScore
        outq.put( (board.peek(), score) )
