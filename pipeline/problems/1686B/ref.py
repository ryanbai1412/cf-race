import sys

data = sys.stdin.buffer.read().split()
idx = 0
t = int(data[idx]); idx += 1
out = []
for _ in range(t):
    n = int(data[idx]); idx += 1
    p = [int(x) for x in data[idx:idx + n]]; idx += n
    ans = 0
    i = 0
    while i + 1 < n:
        if p[i] > p[i + 1]:
            ans += 1
            i += 2
        else:
            i += 1
    out.append(str(ans))
print("\n".join(out))
