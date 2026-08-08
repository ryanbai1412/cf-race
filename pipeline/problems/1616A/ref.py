import sys
from collections import Counter

data = sys.stdin.read().split()
idx = 0
t = int(data[idx]); idx += 1
out = []
for _ in range(t):
    n = int(data[idx]); idx += 1
    a = [int(data[idx + i]) for i in range(n)]; idx += n
    c = Counter(abs(x) for x in a)
    ans = 0
    for v, cnt in c.items():
        if v == 0:
            ans += 1
        else:
            ans += min(cnt, 2)
    out.append(str(ans))
print("\n".join(out))
