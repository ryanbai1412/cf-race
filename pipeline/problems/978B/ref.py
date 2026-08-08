n = int(input())
s = input().strip()
ans = 0
run = 0
for c in s:
    if c == 'x':
        run += 1
    else:
        ans += max(0, run - 2)
        run = 0
ans += max(0, run - 2)
print(ans)
