import sys

data = sys.stdin.read().split()
t = int(data[0])
out = []
for i in range(1, t + 1):
    x = int(data[i])
    low = x & (-x)
    y = low
    if y == x:  # power of two: need xor > 0, add another bit
        y += 2 if low == 1 else 1
    out.append(str(y))
print("\n".join(out))
