n = int(input())
d = input()
s = [int(i) for i in input().split()]
res = "INFINITE"
p = 0
for _ in range(n):
    p += (1 if d[p] == ">" else -1) * s[p]
    if p >= n or p < 0:
        res = "FINITE"
        break
print(res)