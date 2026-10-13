import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

count = a.count(0)

if n > 1:
    if count > 1:
        print("NO")
    else:
        print("YES" if count == 1 else "NO")
else:
    print("NO" if a[0] == 0 else "YES")