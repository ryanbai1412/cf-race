from genlib import *  # noqa: F401,F403
from math import gcd

CHECKER = "Single integer count; unique, exact token comparison."
STATEMENT = "Legend, input (1<=x,y<=1000, 1<=a<=b<=2e9), output present."


def solve(s):
    x, y, a, b = ints(s)
    l = x * y // gcd(x, y)
    return f"{b // l - (a - 1) // l}\n"


def rand(g, hi):
    a = g.randint(1, hi)
    return fmt([g.randint(1, 1000), g.randint(1, 1000), a, g.randint(a, hi)])


def cases(g):
    out = [("boundary", "all ones a=b=1", fmt([1, 1, 1, 1])), ("boundary", "a=b not multiple", fmt([2, 3, 7, 7])),
           ("boundary", "a=b multiple", fmt([2, 3, 6, 6])),
           ("adversarial", "lcm > b (answer 0)", fmt([999, 1000, 1, 998999])),
           ("adversarial", "lcm exactly b", fmt([999, 1000, 1, 999000])),
           ("maxSize", "x=y=1 full range", fmt([1, 1, 1, 2 * 10 ** 9])),
           ("maxSize", "max range coprime large", fmt([997, 991, 1, 2 * 10 ** 9])),
           ("maxSize", "a=b=2e9", fmt([1000, 1000, 2 * 10 ** 9, 2 * 10 ** 9]))]
    out += fill(g, lambda g: rand(g, 2 * 10 ** 9), 70)
    out += fill(g, lambda g: rand(g, 100), 40, reason="small range")
    return out
