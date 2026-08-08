import sys
input = sys.stdin.readline
t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    i = a.index(min(a)); j = a.index(max(a))
    if i > j:
        i, j = j, i
    print(min(j + 1, n - i, (i + 1) + (n - j)))
