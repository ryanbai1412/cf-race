import sys

data = sys.stdin.read().split()
t = int(data[0])
out = []
for i in range(1, t + 1):
    s = data[i]
    out.append(s[1] if len(s) == 2 else min(s))
print("\n".join(out))
