n, m = map(int, input().split())
rows, cols = [], []
for i in range(n):
    s = input()
    for j, ch in enumerate(s):
        if ch == "B":
            rows.append(i)
            cols.append(j)
print((min(rows) + max(rows)) // 2 + 1, (min(cols) + max(cols)) // 2 + 1)
