from collections import Counter

n, a = int(input()), Counter(int(i) for i in input().split())
res = 0
for c in a.values():
    res += c // 2
res //= 2
print(res)