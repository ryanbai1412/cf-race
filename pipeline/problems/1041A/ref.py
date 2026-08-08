input()
a = list(map(int, input().split()))
print(max(a) - min(a) + 1 - len(a))
