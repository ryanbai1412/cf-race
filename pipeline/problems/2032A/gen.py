import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(2032)
w = Writer(sys.argv[1])


def case(n, a):
    return f"{n}\n{' '.join(map(str, a))}"


def rand_case(n=None, p=None):
    n = n or rng.randint(1, 50)
    p = p if p is not None else rng.random()
    return case(n, [1 if rng.random() < p else 0 for _ in range(2 * n)])


# edges
w.add(multi([case(1, [0, 0]), case(1, [1, 0]), case(1, [0, 1]), case(1, [1, 1]),
             case(50, [0] * 100), case(50, [1] * 100),
             case(50, [1] * 50 + [0] * 50), case(50, [1] * 99 + [0])]))
# exhaustive n=1,2 patterns
w.add(multi([case(1, [i, j]) for i in (0, 1) for j in (0, 1)] +
            [case(2, [i, j, k, l]) for i in (0, 1) for j in (0, 1)
             for k in (0, 1) for l in (0, 1)]))
# randoms
for _ in range(12):
    w.add(multi([rand_case() for _ in range(rng.randint(50, 500))]))
for p in (0.05, 0.5, 0.95):
    w.add(multi([rand_case(p=p) for _ in range(500)]))
# max-size: t = 500, n = 50
w.add(multi([rand_case(50) for _ in range(500)]))
w.add(multi([rand_case(50, rng.choice([0.0, 1.0, 0.5])) for _ in range(500)]))
