import chess
import time
import copy

tree = []
tree.append(chess.Move.from_uci("a2a3"))
tree.append(chess.Move.from_uci("a7a6"))
tree.append(chess.Move.from_uci("b2b3"))
tree.append(chess.Move.from_uci("b7b6"))
tree.append(chess.Move.from_uci("c2c3"))
tree.append(chess.Move.from_uci("c7c6"))
tree.append(chess.Move.from_uci("d2d3"))
tree.append(chess.Move.from_uci("d7d6"))

start = time.time()
for i in range(10_000_000):
    forTree = copy.copy(tree)
    forTree.append(chess.Move.from_uci("e2e4"))
    forTree = forTree[:-1]
end = time.time()
execTime = end - start
print("COPY time", round(execTime, 2), "sec")

start = time.time()
for i in range(100_000):
    forTree = copy.deepcopy(tree)
    forTree.append(chess.Move.from_uci("e2e4"))
    forTree = forTree[:-1]
end = time.time()
execTime = (end - start) * 100
print("DEEPCOPY time", round(execTime, 2), "sec")

tree = "a2a3>a7a6>b2b3>b7b6>c2c3>c7c6>d2d3>d7d6>"
move = chess.Move.from_uci("e2e4")
start = time.time()
for i in range(100_000_000):
    forTree = tree
    forTree += move.uci()
    forTree = forTree[:-5]
end = time.time()
execTime = (end - start) / 10
print("STRING time", round(execTime, 2), "sec")

tree = "a2a3>a7a6>b2b3>b7b6>c2c3>c7c6>d2d3>d7d6>"
move = chess.Move.from_uci("e2e4")
start = time.time()
for i in range(100_000_000):
    forTree = tree
    preTree = tree
    forTree += move.uci()
    forTree = preTree
end = time.time()
execTime = (end - start) / 10
print("STRING STATIC time", round(execTime, 2), "sec")