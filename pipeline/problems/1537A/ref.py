import sys
input = sys.stdin.readline
t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    s = sum(a)
    if s == n:
        print(0)
    elif s < n:
        print(1)
    else:
        print(s - n)
