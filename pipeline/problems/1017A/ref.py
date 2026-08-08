import sys

data = sys.stdin.read().split()
n = int(data[0])
sums = []
for i in range(n):
    vals = list(map(int, data[1 + 4 * i : 5 + 4 * i]))
    sums.append(sum(vals))
print(sum(1 for s in sums[1:] if s > sums[0]) + 1)
