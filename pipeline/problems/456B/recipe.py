from genlib import *  # noqa: F401,F403

CHECKER = "Single integer 0..4; unique, exact token comparison."
STATEMENT = "Legend, input (0<=n<=10^(10^5), no leading zeros), output present."


def solve(s):
    t = s.split()[0]
    return ("4" if int(t[-2:]) % 4 == 0 else "0") + "\n"


def num(g, d):
    return str(g.randint(1, 9)) + "".join(g.choice("0123456789") for _ in range(d - 1))


def cases(g):
    out = [("boundary", "n=0", fmt(0)), ("boundary", "n=1", fmt(1)), ("boundary", "n=4", fmt(4)),
           ("adversarial", "last digit divisible by 4 but number not (n=14)", fmt(14)),
           ("adversarial", "n=100 divisible by 4 via last two digits", fmt(100)),
           ("adversarial", "n=10 (last digit 0, not divisible by 4)", fmt(10)),
           ("maxSize", "100000-digit number ending in 12", fmt(num(g, 99998) + "12")),
           ("maxSize", "100000-digit number ending in 98", fmt(num(g, 99998) + "98")),
           ("maxSize", "10^100000 (100001 digits)", fmt("1" + "0" * 100000))]
    out += fill(g, lambda g: fmt(num(g, g.randint(1, 30))), 70)
    out += fill(g, lambda g: fmt(g.randint(0, 200)), 40, reason="small n")
    return out
