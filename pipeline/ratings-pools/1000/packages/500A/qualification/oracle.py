n, t = map(int, input().split())
li = list(map(int, input().split()))
l = 0
while l < t-1:
    l += li[l]
if l==t-1:
    print("YES")
else:
    print("NO")