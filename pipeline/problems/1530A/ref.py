import sys
input = sys.stdin.readline
t = int(input())
for _ in range(t):
    n = input().strip()
    print(max(int(c) for c in n))
