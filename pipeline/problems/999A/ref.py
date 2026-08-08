n, k = map(int, input().split())
a = list(map(int, input().split()))
l, r = 0, n - 1
cnt = 0
while l <= r and a[l] <= k:
    cnt += 1
    l += 1
while r >= l and a[r] <= k:
    cnt += 1
    r -= 1
print(cnt)
