import sys

data = sys.stdin.read().split()
idx = 0
t = int(data[idx]); idx += 1
out = []
for _ in range(t):
    n, l, r, k = (int(data[idx + i]) for i in range(4)); idx += 4
    a = [int(data[idx + i]) for i in range(n)]; idx += n
    ok = sorted(x for x in a if l <= x <= r)
    cnt = 0
    for x in ok:
        if k >= x:
            k -= x
            cnt += 1
        else:
            break
    out.append(str(cnt))
print("\n".join(out))
