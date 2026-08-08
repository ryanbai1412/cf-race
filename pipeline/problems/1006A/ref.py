input()
a = list(map(int, input().split()))
print(" ".join(str(x - 1 if x % 2 == 0 else x) for x in a))
