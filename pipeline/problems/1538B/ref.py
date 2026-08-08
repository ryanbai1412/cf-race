import sys
data = sys.stdin.buffer.read().split()
idx = 0
t = int(data[idx]); idx += 1
res = []
for _ in range(t):
    n = int(data[idx]); idx += 1
    a = data[idx:idx + n]; idx += n
    a = list(map(int, a))
    s = sum(a)
    if s % n:
        res.append(-1)
    else:
        avg = s // n
        res.append(sum(1 for x in a if x > avg))
print("\n".join(map(str, res)))
