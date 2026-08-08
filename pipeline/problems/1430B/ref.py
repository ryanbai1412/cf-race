import sys

data = sys.stdin.buffer.read().split()
pos = 0
t = int(data[pos]); pos += 1
out = []
for _ in range(t):
    n, k = int(data[pos]), int(data[pos + 1]); pos += 2
    a = [int(x) for x in data[pos:pos + n]]; pos += n
    a.sort(reverse=True)
    out.append(str(sum(a[:k + 1])))
print("\n".join(out))
