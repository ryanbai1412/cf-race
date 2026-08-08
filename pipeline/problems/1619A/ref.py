import sys

data = sys.stdin.read().split()
t = int(data[0])
out = []
for i in range(1, t + 1):
    s = data[i]
    n = len(s)
    if n % 2 == 0 and s[:n // 2] == s[n // 2:]:
        out.append("YES")
    else:
        out.append("NO")
print("\n".join(out))
