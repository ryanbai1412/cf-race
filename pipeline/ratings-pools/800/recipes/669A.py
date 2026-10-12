from rlib import *

CONSTRAINTS = "a single integer n with 1 <= n <= 10^9."
UNIQUENESS = "Unique integer."
STATEMENT = "Reviewed full statement: alternate 1,2 gives n//3*2 + (n%3 != 0); brute-force checked for n < 40."


def validate(inp):
    num(exact_tokens(inp, 1)[0], 1, 10 ** 9)


def solve(inp):
    n = int(inp.split()[0])
    return str(n // 3 * 2 + (1 if n % 3 else 0))


def brute(n):
    best = {}
    def go(rem, last):
        key = (rem, last)
        if key in best:
            return best[key]
        r = max([1 + go(rem - k, k) for k in range(1, rem + 1) if k != last] or [0])
        best[key] = r
        return r
    return go(n, 0)


def extra():
    for n in range(1, 40):
        assert solve(str(n)) == str(brute(n))
    return [("boundary", "n=1", "1\n"), ("boundary", "n=2", "2\n"), ("adversarial", "n=3", "3\n"),
            ("maxSize", "n=10^9", "1000000000\n"), ("maxSize", "n=999999999", "999999999\n")]
