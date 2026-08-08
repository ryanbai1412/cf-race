from collections import Counter

input()
a = list(map(int, input().split()))
print(max(Counter(a).values()))
