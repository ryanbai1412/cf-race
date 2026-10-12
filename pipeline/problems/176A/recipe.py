from genlib import *  # noqa: F401,F403

CHECKER = "Single maximum integer; unique, exact token comparison."
STATEMENT = "Legend (buy on one planet, sell on another, hold capacity k), input (2<=n<=10, 1<=m,k<=100, 1<=b<a<=1000, 0<=c<=100), output present."
LOW = "abcdefghijklmnopqrstuvwxyz"


def solve(s):
    t = s.split()
    n, m, k = map(int, t[:3])
    p, pos = [], 3
    for _ in range(n):
        pos += 1
        p.append([tuple(map(int, t[pos + 3 * j:pos + 3 * j + 3])) for j in range(m)])
        pos += 3 * m
    best = 0
    for i in range(n):
        for j in range(n):
            if i != j:
                gains = sorted((p[j][x][1] - p[i][x][0], p[i][x][2]) for x in range(m) if p[j][x][1] > p[i][x][0])
                cap, prof = k, 0
                for gain, cnt in reversed(gains):
                    take = min(cap, cnt)
                    prof += take * gain
                    cap -= take
                best = max(best, prof)
    return f"{best}\n"


def make(g, n, m, k, hi=1000, cmax=100):
    names = set()
    while len(names) < n:
        names.add(g.choice(LOW).upper() + "".join(g.choice(LOW) for _ in range(g.randint(0, 9))))
    rows = [[n, m, k]]
    for nm in sorted(names, key=lambda _: g.random()):
        rows.append(nm)
        for _ in range(m):
            a = g.randint(2, hi)
            rows.append([a, g.randint(1, a - 1), g.randint(0, cmax)])
    return fmt(*rows)


def cases(g):
    out = [("boundary", "n=2 m=k=1 no profit", fmt([2, 1, 1], "A", [2, 1, 1], "B", [2, 1, 1])),
           ("boundary", "n=2 m=k=1 profit 998", fmt([2, 1, 1], "A", [2, 1, 1], "B", [1000, 999, 0])),
           ("adversarial", "zero stock of best item", fmt([2, 2, 5], "Aa", [2, 1, 0], [5, 1, 10], "Bb", [1000, 900, 0], [10, 9, 0])),
           ("maxSize", "n=10 m=k=100", make(g, 10, 100, 100)), ("maxSize", "n=10 m=100 k=100 low stock", make(g, 10, 100, 100, cmax=2))]
    out += fill(g, lambda g: make(g, g.randint(2, 4), g.randint(1, 4), g.randint(1, 10), 20, 5), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(2, 10), g.randint(1, 30), g.randint(1, 100)), 30)
    return out
