from genlib import *  # noqa: F401,F403

CHECKER = "Single integer count of sessions; unique, exact token comparison."
STATEMENT = "Legend (each session raises one soldier of every distinct rank < k), input (1<=n,k<=100, non-decreasing 1<=ai<=k), output present."


def solve(s):
    v = ints(s)
    k, a = v[1], v[2:]
    sessions = 0
    while any(x < k for x in a):
        seen, nxt = set(), []
        for x in a:
            if x < k and x not in seen:
                seen.add(x)
                nxt.append(x + 1)
            else:
                nxt.append(x)
        a = sorted(nxt)
        sessions += 1
    return f"{sessions}\n"


def make(g, n, k):
    return fmt([n, k], sorted(g.randint(1, k) for _ in range(n)))


def cases(g):
    out = [("boundary", "n=k=1", fmt([1, 1], [1])), ("boundary", "all already max", fmt([3, 5], [5, 5, 5])),
           ("adversarial", "all equal rank 1", fmt([4, 3], [1, 1, 1, 1])),
           ("maxSize", "n=k=100 all 1 (max sessions)", fmt([100, 100], [1] * 100)), ("maxSize", "n=k=100 random", make(g, 100, 100)),
           ("maxSize", "n=100 k=1", fmt([100, 1], [1] * 100))]
    out += fill(g, lambda g: make(g, g.randint(1, 6), g.randint(1, 6)), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 100), g.randint(1, 100)), 30)
    return out
