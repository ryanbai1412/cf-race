import sys

data = sys.stdin.read().split()
t = int(data[0])
out = []
for i in range(1, t + 1):
    s = data[i]
    out.append("NO" if s.count("N") == 1 else "YES")
print("\n".join(out))
