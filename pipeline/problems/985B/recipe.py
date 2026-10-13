from genlib import *  # noqa: F401,F403

CHECKER = "YES/NO; unique, exact token comparison."
STATEMENT = "Legend (ignore one switch, still all lamps on), input (1<=n,m<=2000, 0/1 matrix, all switches cover all lamps), output present."


def solve(s):
    t = s.split()
    n, m = int(t[0]), int(t[1])
    rows = t[2:2 + n]
    cnt = [col.count("1") for col in zip(*rows)]
    for r in rows:
        if all(cnt[j] >= 2 for j, c in enumerate(r) if c == "1"):
            return "YES\n"
    return "NO\n"


def make(g, n, m, p):
    rows = [["1" if g.random() < p else "0" for _ in range(m)] for _ in range(n)]
    for j in range(m):
        if not any(r[j] == "1" for r in rows):
            rows[g.randrange(n)][j] = "1"
    return fmt([n, m], *["".join(r) for r in rows])


def cases(g):
    out = [("boundary", "n=m=1 (NO)", fmt([1, 1], "1")), ("boundary", "n=2 duplicate", fmt([2, 1], "1", "1")),
           ("adversarial", "identity (NO)", fmt([3, 3], "100", "010", "001")), ("adversarial", "extra zero switch", fmt([2, 2], "11", "00")),
           ("maxSize", "2000x2000 identity-ish (NO)", fmt([2000, 2000], *["0" * i + "1" + "0" * (1999 - i) for i in range(2000)])),
           ("maxSize", "2000x300 random dense", make(g, 2000, 300, 0.5)), ("maxSize", "1x2000 all ones", fmt([1, 2000], "1" * 2000))]
    out += fill(g, lambda g: make(g, g.randint(1, 5), g.randint(1, 5), g.random() / 2), 90, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(6, 60), g.randint(6, 60), g.random() / 8), 25)
    return out
