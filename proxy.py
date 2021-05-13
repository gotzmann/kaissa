from log import log
from subprocess import PIPE, Popen
from threading  import Thread
from queue import Queue, Empty

def inProcess(stdin, queue):
    while True:
        msg = queue.get()
        stdin.write(msg + "\n")
        stdin.flush()

def outProcess(stdout, queue):
    while True:
        for line in iter(stdout.readline, b''):
            print(line.rstrip())

process = Popen(['sos.exe'], text=True, bufsize=0, stdin=PIPE, stdout=PIPE)

queue = Queue()
t1 = Thread(target=inProcess, args=(process.stdin, queue))
t1.daemon = True # thread dies with the program
t1.start()

t2 = Thread(target=outProcess, args=(process.stdout, queue))
t2.daemon = True # thread dies with the program
t2.start()

while True:

    msg = input()
    log(f">>> {msg}", "proxy.log")    
    if msg == "quit": break
    queue.put(msg)

process.terminate()
