import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(15602)
w = Writer(sys.argv[1])
MAXT = 10000
MAXV = 10 ** 8


def case(a, b, c):
    return f"{a} {b} {c}"


def distinct_random(hi):
    while True:
        a, b, c = (rng.randint(1, hi) for _ in range(3))
        if a != b and b != c and a != c:
            return a, b, c


def valid_case(n):
    """a,b opposite in a circle of n people; c anywhere in 1..n."""
    h = n // 2
    a = rng.randint(1, n)
    b = (a + h - 1) % n + 1
    c = rng.randint(1, n)
    while c in (a, b):
        c = rng.randint(1, n)
    return case(a, b, c)


# tiny exhaustive-ish: all distinct triples from 1..6
w.add(multi([case(a, b, c) for a in range(1, 7) for b in range(1, 7)
             for c in range(1, 7) if a != b and b != c and a != c]))
# extremes at the value bound
ex = [1, 2, MAXV // 2, MAXV // 2 + 1, MAXV - 1, MAXV]
w.add(multi([case(a, b, c) for a in ex for b in ex for c in ex
             if a != b and b != c and a != c]))
# max t: valid circles of maximum size
w.add(multi([valid_case(MAXV) for _ in range(MAXT)]))
# max t: valid circles of random even size
w.add(multi([valid_case(2 * rng.randint(1, MAXV // 2)) for _ in range(MAXT)]))
# max t: valid circle but c may be out of range
cases = []
for _ in range(MAXT):
    n = 2 * rng.randint(1, MAXV // 2)
    h = n // 2
    a = rng.randint(1, n)
    b = (a + h - 1) % n + 1
    c = rng.randint(1, MAXV)
    if a != b and b != c and a != c:
        cases.append(case(a, b, c))
w.add(multi(cases))
# max t: fully random (mostly -1)
w.add(multi([case(*distinct_random(MAXV)) for _ in range(MAXT)]))
# max t: fully random small (mix of valid and invalid)
w.add(multi([case(*distinct_random(20)) for _ in range(MAXT)]))
w.add(multi([case(*distinct_random(6)) for _ in range(MAXT)]))
# near misses: |a-b| off by one from a valid configuration
cases = []
for _ in range(MAXT):
    n = 2 * rng.randint(2, 10 ** 7)
    h = n // 2
    a = rng.randint(1, n)
    b = (a + h - 1) % n + 1 + rng.choice([-1, 1])
    c = rng.randint(1, n)
    if 1 <= b <= MAXV and a != b and b != c and a != c:
        cases.append(case(a, b, c))
w.add(multi(cases))
# neighbours / adjacent numbers (small circles)
w.add(multi([case(a, a + 1, c) for a in range(1, 200)
             for c in range(1, 6) if c != a and c != a + 1]))
# single cases
w.add(f"1\n{MAXV // 2} {MAXV} 1\n")
w.add("1\n1 2 3\n")
