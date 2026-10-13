n, a = int(input()), (int(i) for i in input().split())
last, res, longest = {e: i for i, e in enumerate(a)}, 0, 0
for e, i in last.items():
    if n - i > longest:
        res, longest = e, n - i
print(res)