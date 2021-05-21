from log import log
from subprocess import PIPE, Popen
from threading  import Thread
from queue import Queue, Empty
import sys

engine = "C:\\git\\kaissa64\\engines\\" + sys.argv[1]     
depth = sys.argv[2]
cmd = [ engine ]

def inProcess(stdin, queue):
    while True:
        msg = queue.get()

        # Hacking Arena :)
        if msg[0:2] == "go":
            msg += f" depth {depth}"
            log(f"[:] {msg}", "proxy.log")                    

        stdin.write(msg + "\n")
        stdin.flush()

def outProcess(stdout, queue):
    while True:
        for line in iter(stdout.readline, b''):
            log(f"{line.rstrip()}", "proxy.log")        
            print(line.rstrip(), flush=True)

process = Popen(cmd, text=True, stdin=PIPE, stdout=PIPE)

queue = Queue()
t1 = Thread(target=inProcess, args=(process.stdin, queue))
t1.daemon = True # thread dies with the program
t1.start()

t2 = Thread(target=outProcess, args=(process.stdout, queue))
t2.daemon = True # thread dies with the program
t2.start()

log(f"\n[START]\n", "proxy.log")        

while True:

    msg = input()
    log(f">>> {msg}", "proxy.log")        
    queue.put(msg)
    if msg == "quit": break

process.terminate()

log(f"\n[FINISH]\n", "proxy.log")        
