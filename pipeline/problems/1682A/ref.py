import sys

data = sys.stdin.read().split()
idx = 0
t = int(data[idx]); idx += 1
out = []
for _ in range(t):
    n = int(data[idx]); idx += 1
    s = data[idx]; idx += 1
    c = s[(n - 1) // 2]
    cnt = 0
    i = (n - 1) // 2
    while i >= 0 and s[i] == c:
        cnt += 1
        i -= 1
    j = (n - 1) // 2 + 1
    while j < n and s[j] == c:
        cnt += 1
        j += 1
    out.append(str(cnt))
print("\n".join(out))
