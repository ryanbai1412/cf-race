import sys

n, m, k = map(int, sys.stdin.read().split())
print("Yes" if m >= n and k >= n else "No")
