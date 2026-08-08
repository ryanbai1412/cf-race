import sys

data = sys.stdin.buffer.read().split()
pos = 0
t = int(data[pos]); pos += 1
out = []
for _ in range(t):
    n = int(data[pos]); pos += 1
    a = sorted(int(x) for x in data[pos:pos + n]); pos += n
    best = 0
    for i, m in enumerate(a):
        best = max(best, m * (n - i))
    out.append(str(best))
print("\n".join(out))
