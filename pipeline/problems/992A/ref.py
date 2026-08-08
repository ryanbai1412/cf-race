n = int(input())
a = list(map(int, input().split()))
print(len(set(x for x in a if x != 0)))
