import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1542)
w = Writer(sys.argv[1])


def case(a) -> str:
    n = len(a) // 2
    return f"{n}\n" + " ".join(map(str, a))


def rand_case(n, lo=0, hi=100):
    return case([rng.randint(lo, hi) for _ in range(2 * n)])


def balanced(n):
    """exactly n odds and n evens -> Yes"""
    a = [rng.randrange(1, 100, 2) for _ in range(n)] + \
        [rng.randrange(0, 101, 2) for _ in range(n)]
    rng.shuffle(a)
    return case(a)


# edge: n=1
w.add(multi([case([0, 0]), case([0, 1]), case([1, 1]), case([100, 99])]))
# all zeros / all max, all same parity
w.add(multi([case([0] * 200), case([100] * 200), case([99] * 200),
             case([1] * 2), case([2] * 2)]))
# balanced (all Yes) at max n
w.add(multi([balanced(100) for _ in range(100)]))
# off-by-one from balanced (all No)
cases = []
for _ in range(100):
    n = rng.randint(1, 100)
    a = [rng.randrange(1, 100, 2) for _ in range(n + 1)] + \
        [rng.randrange(0, 101, 2) for _ in range(n - 1)]
    rng.shuffle(a)
    cases.append(case(a))
w.add(multi(cases))
# random mixes
for _ in range(6):
    w.add(multi([rand_case(rng.randint(1, 100)) for _ in range(100)]))
# small values only (0/1)
w.add(multi([case([rng.randint(0, 1) for _ in range(2 * rng.randint(1, 100))])
             for _ in range(100)]))
# max-size: t=100, n=100 all random
w.add(multi([rand_case(100) for _ in range(100)]))
w.add(multi([balanced(100) if i % 2 else rand_case(100) for i in range(100)]))
