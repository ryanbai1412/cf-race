import sys

x = int(sys.stdin.read().split()[0])
order = ["A", "B", "C", "D"]


def cat(v):
    r = v % 4
    return "A" if r == 1 else "B" if r == 3 else "C" if r == 2 else "D"


best_a, best_c = None, None
for a in range(3):
    c = cat(x + a)
    if best_c is None or order.index(c) < order.index(best_c):
        best_a, best_c = a, c
print(best_a, best_c)
