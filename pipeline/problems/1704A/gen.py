import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1704)
w = Writer(sys.argv[1])


def case(a, b):
    return f"{len(a)} {len(b)}\n{a}\n{b}"


def rand_bits(n):
    return "".join(rng.choice("01") for _ in range(n))


def yes_case(n, m):
    """construct a guaranteed-YES case"""
    b = rand_bits(m)
    prefix = rand_bits(n - m)
    # ensure b[0] appears in a[:n-m+1]
    a = prefix + b[0] + b[1:]
    return case(a, b)


# edge: n=m equal/unequal, m=1, single chars
w.add(multi([
    case("0", "0"), case("1", "1"), case("0", "1"), case("1", "0"),
    case("01", "01"), case("01", "10"),
    case("10", "0"), case("10", "1"), case("00", "1"), case("11", "0"),
]))
# m=1 cases: answer depends only on presence of b[0] in a
w.add(multi([case(rand_bits(rng.randint(1, 50)), rand_bits(1)) for _ in range(500)]))
# all-zeros / all-ones combos
w.add(multi([
    case("0" * 50, "0" * 50), case("1" * 50, "1" * 50),
    case("0" * 50, "0" * 25), case("1" * 50, "0" * 25),
    case("0" * 49 + "1", "1"), case("1" + "0" * 49, "1" * 2),
]))
# guaranteed YES cases
for _ in range(2):
    cases = []
    for _ in range(500):
        n = rng.randint(1, 50)
        m = rng.randint(1, n)
        cases.append(yes_case(n, m))
    w.add(multi(cases))
# random (mixed verdicts)
for _ in range(4):
    cases = []
    for _ in range(500):
        n = rng.randint(1, 50)
        m = rng.randint(1, n)
        cases.append(case(rand_bits(n), rand_bits(m)))
    w.add(multi(cases))
# near-miss: suffix matches but b[0] missing from window
cases = []
for _ in range(500):
    n = rng.randint(2, 50)
    m = rng.randint(1, n - 1)
    b = rand_bits(m)
    other = "1" if b[0] == "0" else "0"
    a = other * (n - m + 1) + b[1:]
    cases.append(case(a, b))
w.add(multi(cases))
# max t, max sizes
w.add(multi([case(rand_bits(50), rand_bits(rng.randint(1, 50))) for _ in range(2000)]))
