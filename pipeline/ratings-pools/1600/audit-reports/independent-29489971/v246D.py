import sys
raw = sys.stdin.buffer.read().decode()
t = raw.replace("\r\n", "\n")
assert "\r" not in t and "\t" not in t, "bad ws"
lines = t.split("\n")
if lines and lines[-1] == "": lines.pop()
def ints(l, k):
    p = l.split(" "); assert len(p) == k and all(x and (x == "0" or x[0] != "0") and x.isdigit() for x in p), ("line", l[:50]); return list(map(int, p))
n, m = ints(lines[0], 2)
assert 1 <= n <= 100000 and 1 <= m <= 100000, "nm"
assert len(lines) == 2 + m, ("linecount", len(lines), m)
c = ints(lines[1], n); assert all(1 <= x <= 100000 for x in c), "c"
seen = set(); nb = {}
for i in range(m):
    a, b = ints(lines[2 + i], 2)
    assert 1 <= a <= n and 1 <= b <= n and a != b, "edge"
    e = (min(a, b), max(a, b)); assert e not in seen, "dup"; seen.add(e)
    x, y = c[a - 1], c[b - 1]
    if x != y:
        nb.setdefault(x, set()).add(y); nb.setdefault(y, set()).add(x)
print(min(set(c), key=lambda k: (-len(nb.get(k, ())), k)))
