import sys

data = sys.stdin.read().split()
idx = 0
t = int(data[idx]); idx += 1
out = []
for _ in range(t):
    n, m, k = int(data[idx]), int(data[idx + 1]), int(data[idx + 2])
    idx += 3
    a = sorted(data[idx]); idx += 1
    b = sorted(data[idx]); idx += 1
    i = j = 0
    run_a = run_b = 0
    c = []
    while i < len(a) and j < len(b):
        take_a = a[i] < b[j]
        if take_a and run_a == k:
            take_a = False
        elif not take_a and run_b == k:
            take_a = True
        if take_a:
            c.append(a[i]); i += 1
            run_a += 1; run_b = 0
        else:
            c.append(b[j]); j += 1
            run_b += 1; run_a = 0
    out.append("".join(c))
print("\n".join(out))
