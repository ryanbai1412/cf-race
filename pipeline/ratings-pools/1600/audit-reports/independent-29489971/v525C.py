import sys
t = sys.stdin.buffer.read().decode().replace("\r\n", "\n")
assert "\r" not in t and "\t" not in t, "bad ws"
lines = t.split("\n")
if lines and lines[-1] == "": lines.pop()
assert len(lines) == 2, "linecount"
def ints(l, k):
    p = l.split(" "); assert len(p) == k and all(x.isdigit() and x[0] != "0" for x in p), ("line", l[:50]); return list(map(int, p))
n, = ints(lines[0], 1); assert 1 <= n <= 100000
a = ints(lines[1], n); assert all(2 <= x <= 1000000 for x in a)
a.sort(reverse=True)
sides = []; i = 0
while i + 1 < n:
    if a[i] - a[i + 1] <= 1: sides.append(a[i + 1]); i += 2
    else: i += 1
print(sum(sides[j] * sides[j + 1] for j in range(0, len(sides) - 1, 2)))
