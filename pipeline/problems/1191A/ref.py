import sys

x = int(sys.stdin.read().split()[0])
RANK = {1: 0, 3: 1, 2: 2, 0: 3}
NAME = {1: "A", 3: "B", 2: "C", 0: "D"}
best = min(range(3), key=lambda a: RANK[(x + a) % 4])
print(best, NAME[(x + best) % 4])
