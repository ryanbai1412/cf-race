n, m = map(int, input().split())
c = list(map(int, input().split()))
a = list(map(int, input().split()))
j = 0
bought = 0
for cost in c:
    if j < m and a[j] >= cost:
        j += 1
        bought += 1
print(bought)
