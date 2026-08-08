import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1417)
w = Writer(sys.argv[1])
KMAX = 10 ** 4


def case(k, a):
    assert 2 <= len(a) <= 1000 and 2 <= k <= KMAX and all(1 <= x <= k for x in a)
    return f"{len(a)} {k}\n" + " ".join(map(str, a))


def pack(cases):
    """Respect sum(n) <= 1000 and sum(k) <= 10^4."""
    return multi(cases)


def rand_case(n, k):
    return case(k, [rng.randint(1, k) for _ in range(n)])


# edges (small n and k so the sums stay legal)
w.add(pack([case(2, [1, 1]), case(2, [2, 2]), case(10 ** 4, [1, 1]),
            case(10 ** 4, [10 ** 4, 10 ** 4]),
            case(10 ** 4, [1] * 100), case(9999, [3, 9999, 7])]))
# one max case: n = 1000, k = 10^4
w.add(pack([case(KMAX, [rng.randint(1, KMAX) for _ in range(1000)])]))
w.add(pack([case(KMAX, [1] * 1000)]))
w.add(pack([case(KMAX, [KMAX] * 1000)]))
w.add(pack([case(KMAX, [1] + [KMAX] * 999)]))
w.add(pack([case(KMAX, [KMAX // 2] * 1000)]))
# many small cases: 500 cases of n=2, k=20 (sum n = 1000, sum k = 10^4)
for _ in range(4):
    w.add(pack([rand_case(2, 20) for _ in range(500)]))
# 200 cases of n=5, k=50
for _ in range(3):
    w.add(pack([rand_case(5, 50) for _ in range(200)]))
# 100 cases of n=10, k=100
for _ in range(3):
    w.add(pack([rand_case(10, 100) for _ in range(100)]))
# 10 cases n=100 k=1000
for _ in range(2):
    w.add(pack([rand_case(100, 1000) for _ in range(10)]))
# min-heavy: min value 1 forces large answers
w.add(pack([case(KMAX, [1] + [rng.randint(1, KMAX) for _ in range(999)])]))
