import sys
from collections import Counter

data = sys.stdin.read().split()
t = int(data[0])
out = []
idx = 1
for _ in range(t):
    s = data[idx]; T = data[idx + 1]; idx += 2
    c = Counter(s)
    if T == "abc" and c["a"] > 0 and c["b"] > 0 and c["c"] > 0:
        res = "a" * c["a"] + "c" * c["c"] + "b" * c["b"] + "".join(
            ch * c[ch] for ch in sorted(c) if ch > "c")
    else:
        res = "".join(sorted(s))
    out.append(res)
print("\n".join(out))
