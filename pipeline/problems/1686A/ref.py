import sys

data = sys.stdin.read().split()
idx = 0
t = int(data[idx]); idx += 1
out = []
for _ in range(t):
    n = int(data[idx]); idx += 1
    a = [int(x) for x in data[idx:idx + n]]; idx += n
    s = sum(a)
    out.append("YES" if any(x * n == s for x in a) else "NO")
print("\n".join(out))
