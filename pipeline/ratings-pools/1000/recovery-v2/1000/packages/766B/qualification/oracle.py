a = int(input())
b = list(map(int, input().split()))
b.sort()
ans = 0
for i in range(1,a - 1):
    if b[i] + b[i - 1] > b[i + 1]:
        ans += 1
if ans > 0:
    print("YES")
else:
    print("NO")