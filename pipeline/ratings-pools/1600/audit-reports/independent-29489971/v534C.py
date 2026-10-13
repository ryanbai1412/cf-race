import sys
t = sys.stdin.buffer.read().decode().replace("\r\n", "\n")
assert "\r" not in t and "\t" not in t, "bad ws"
lines = t.split("\n")
if lines and lines[-1] == "": lines.pop()
assert len(lines) == 2, "linecount"
def ints(l, k):
    p = l.split(" "); assert len(p) == k and all(x.isdigit() and x[0] != "0" for x in p), ("line", l[:50]); return list(map(int, p))
n, A = ints(lines[0], 2)
d = ints(lines[1], n)
S = sum(d)
assert 1 <= n <= 200000 and all(1 <= x <= 1000000 for x in d) and n <= A <= S, "range"
out = []
for x in d:
    lo = max(1, A - (S - x)); hi = min(x, A - (n - 1))
    out.append(x - (hi - lo + 1))
print(" ".join(map(str, out)))
