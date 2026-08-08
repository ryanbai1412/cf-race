n, m = map(int, input().split())
x = input().split()
y = set(input().split())
res = [d for d in x if d in y]
print(" ".join(res))
