import sys


def distinct(x: int) -> bool:
    s = str(x)
    return len(set(s)) == len(s)


l, r = map(int, sys.stdin.read().split())
for x in range(l, r + 1):
    if distinct(x):
        print(x)
        break
else:
    print(-1)
