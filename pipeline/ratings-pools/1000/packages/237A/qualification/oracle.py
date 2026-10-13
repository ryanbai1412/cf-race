n = int(input())
events = []

for _ in range(n):
    h, m = map(int, input().split())
    events.append((h * 60 + m, 1))
    events.append((h * 60 + m + 1, 0))
events.sort()

min_cash = 0
current_cust = 0
for _, event in events:
    if event == 1:
        current_cust += 1
        min_cash = max(min_cash, current_cust)
    else:
        current_cust -= 1
print(min_cash)