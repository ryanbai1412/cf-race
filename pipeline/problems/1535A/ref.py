import sys
input = sys.stdin.readline
t = int(input())
for _ in range(t):
    s = list(map(int, input().split()))
    w1 = max(s[0], s[1]); w2 = max(s[2], s[3])
    top2 = sorted(s)[2:]
    print("YES" if sorted([w1, w2]) == top2 else "NO")
