import sys

data = sys.stdin.read().split()
t = int(data[0])
out = []
idx = 1
for _ in range(t):
    a = int(data[idx]); b = int(data[idx + 1]); idx += 2
    out.append(str(min(a, b, (a + b) // 4)))
print("\n".join(out))
