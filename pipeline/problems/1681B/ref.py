import sys

data = sys.stdin.buffer.read().split()
idx = 0
t = int(data[idx]); idx += 1
out = []
for _ in range(t):
    n = int(data[idx]); idx += 1
    a = data[idx:idx + n]; idx += n
    m = int(data[idx]); idx += 1
    s = sum(int(x) for x in data[idx:idx + m]); idx += m
    out.append(a[s % n].decode())
print("\n".join(out))
