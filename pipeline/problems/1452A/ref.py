import sys

data = sys.stdin.read().split()
t = int(data[0])
out = []
for i in range(t):
    x = int(data[1 + 2 * i])
    y = int(data[2 + 2 * i])
    lo, hi = min(x, y), max(x, y)
    if lo == hi:
        out.append(str(2 * lo))
    else:
        out.append(str(2 * hi - 1))
print("\n".join(out))
