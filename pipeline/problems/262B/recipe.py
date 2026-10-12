from genlib import *  # noqa: F401,F403

CHECKER = "Single maximum integer; unique, exact token comparison."
STATEMENT = "Legend (exactly k sign changes), input (1<=n,k<=1e5, sorted, |ai|<=1e4), output present."


def solve(s):
    v = ints(s)
    n, k = v[0], v[1]
    a = v[2:]
    for i in range(n):
        if k and a[i] < 0:
            a[i] = -a[i]
            k -= 1
    total = sum(a)
    if k % 2:
        total -= 2 * min(abs(x) for x in a)
    return f"{total}\n"


def make(g, n, k, hi):
    return fmt([n, k], sorted(g.randint(-hi, hi) for _ in range(n)))


def cases(g):
    out = [("boundary", "n=k=1 positive", fmt([1, 1], [5])), ("boundary", "n=1 zero", fmt([1, 1], [0])),
           ("adversarial", "k larger than negatives, odd remainder", fmt([3, 4], [-3, -2, 5])),
           ("adversarial", "remainder absorbed by zero", fmt([3, 5], [-2, 0, 1])),
           ("maxSize", "n=k=1e5 all -1e4", fmt([100000, 100000], [-10000] * 100000)),
           ("maxSize", "n=1e5 k=99999 random", make(g, 100000, 99999, 10000))]
    out += fill(g, lambda g: make(g, g.randint(1, 8), g.randint(1, 10), 5), 80, reason="small random")
    out += fill(g, lambda g: make(g, g.randint(1, 3000), g.randint(1, 10 ** 5), 10000), 30)
    return out
