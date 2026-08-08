import sys

n, m, k = map(int, sys.stdin.read().split())
ok = True
pens, nb = m, k
for _ in range(n):
    if pens <= 0 or nb <= 0:
        ok = False
        break
    pens -= 1
    nb -= 1
print("Yes" if ok else "No")
