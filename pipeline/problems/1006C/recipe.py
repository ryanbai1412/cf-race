from genlib import *  # noqa: F401,F403

CHECKER = "Single maximum integer; unique, exact token comparison."
STATEMENT = "Legend (three contiguous parts, sum1=sum3 maximal), input (1<=n<=2e5, 1<=di<=1e9), output present."


def solve(s):
    v = ints(s)
    d = v[1:]
    i, j, s1, s3, best = 0, len(d) - 1, 0, 0, 0
    while i <= j:
        if s1 <= s3:
            s1 += d[i]
            i += 1
        else:
            s3 += d[j]
            j -= 1
        if s1 == s3:
            best = s1
    return f"{best}\n"


def arr(g, n, hi):
    return fmt(n, [g.randint(1, hi) for _ in range(n)])


def cases(g):
    B = 10 ** 9
    out = [("boundary", "n=1 (0)", fmt(1, [B])), ("boundary", "n=2 equal", fmt(2, [7, 7])),
           ("adversarial", "all ones odd length", fmt(5, [1] * 5)), ("adversarial", "all equal even length", fmt(4, [5, 5, 5, 5])),
           ("maxSize", "n=2e5 all 1e9 (sum 1e14)", fmt(200000, [B] * 200000)), ("maxSize", "n=2e5 random small", arr(g, 200000, 3)),
           ("maxSize", "n=2e5 random large", arr(g, 200000, B))]
    out += fill(g, lambda g: arr(g, g.randint(1, 10), 3), 80, reason="small random")
    out += fill(g, lambda g: arr(g, g.randint(1, 3000), g.choice([2, B])), 30)
    return out
