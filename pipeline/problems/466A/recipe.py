from genlib import *  # noqa: F401,F403

CHECKER = "Single minimum integer cost; unique value, exact token comparison."
STATEMENT = "Full legend, input (n,m,a,b in [1,1000]), output and note present in the pinned source row."


def solve(s):
    n, m, a, b = ints(s)
    return str(min(n * a, n // m * b + min(n % m * a, b))) + "\n"


def cases(g):
    out = [
        ("boundary", "all parameters minimal (1 1 1 1)", fmt([1, 1, 1, 1])),
        ("boundary", "m > n: one m-ticket cheaper than n singles", fmt([3, 1000, 1000, 1])),
        ("boundary", "n == m", fmt([7, 7, 3, 20])),
        ("adversarial", "remainder cheaper as an extra m-ticket than singles", fmt([1000, 999, 1000, 2])),
        ("adversarial", "m-ticket never worth it (b >= m*a)", fmt([1000, 7, 1, 1000])),
        ("adversarial", "tie b == m*a", fmt([10, 3, 2, 6])),
        ("maxSize", "all parameters maximal", fmt([1000, 1000, 1000, 1000])),
        ("maxSize", "n maximal, singles maximal, cheap m=1 ticket", fmt([1000, 1, 1000, 1])),
    ]
    out += fill(g, lambda g: fmt([g.randint(1, 1000) for _ in range(4)]), 60)
    out += fill(g, lambda g: fmt([g.randint(1, 30) for _ in range(4)]), 60, reason="small random")
    return out
