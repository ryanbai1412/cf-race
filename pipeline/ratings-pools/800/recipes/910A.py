from rlib import *

CONSTRAINTS = "n in 2..100, d in 1..n-1; binary string of length n starting and ending with 1."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: minimum jumps (<= d) on lilies, -1 if impossible."


def validate(inp):
    t = exact_tokens(inp, 3)
    n = num(t[0], 2, 100); num(t[1], 1, n - 1)
    word(t[2], "01", n, n)
    need(t[2][0] == "1" and t[2][-1] == "1", "ends are lilies")


def solve(inp):
    n, d, s = inp.split()
    n, d = int(n), int(d)
    dist = [-1] * n
    dist[0] = 0
    for i in range(n):
        if dist[i] < 0:
            continue
        for j in range(i + 1, min(n, i + d + 1)):
            if s[j] == "1" and (dist[j] < 0 or dist[j] > dist[i] + 1):
                dist[j] = dist[i] + 1
    return str(dist[-1])


def extra():
    return [("boundary", "n=2 d=1", "2 1\n11\n"), ("adversarial", "gap too wide", "4 2\n1001\n"),
            ("maxSize", "n=100 d=1 all lilies (99 jumps)", "100 1\n" + "1" * 100 + "\n"),
            ("maxSize", "n=100 d=99 single jump", "100 99\n1" + "0" * 98 + "1\n")]
