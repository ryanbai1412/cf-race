n = int(input())
cnt = 0
for d in (100, 20, 10, 5, 1):
    cnt += n // d
    n %= d
print(cnt)
