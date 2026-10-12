from genlib import *  # noqa: F401,F403

CHECKER = "Single maximum integer; unique, exact token comparison."
STATEMENT = "Legend (at most k swaps maximizing inversions), input (1<=n,k<=1e5), output present."


def solve(s):
    n, k = ints(s)
    return f"{sum(2 * (n - 2 * i) + 1 for i in range(1, min(k, n // 2) + 1))}\n"


def cases(g):
    N = 10 ** 5
    out = [("boundary", "n=1", fmt([1, 1])), ("boundary", "n=2 k=1", fmt([2, 1])), ("boundary", "n=1 k=1e5", fmt([1, N])),
           ("adversarial", "k exactly n/2", fmt([10, 5])), ("adversarial", "odd n, k=(n-1)/2", fmt([11, 5])),
           ("maxSize", "n=k=1e5 (reverse, 64-bit)", fmt([N, N])), ("maxSize", "n=1e5 k=1", fmt([N, 1])), ("maxSize", "n=1e5 k=49999", fmt([N, 49999]))]
    out += fill(g, lambda g: fmt([g.randint(1, 12), g.randint(1, 12)]), 80, reason="small random")
    out += fill(g, lambda g: fmt([g.randint(1, N), g.randint(1, N)]), 40)
    return out
