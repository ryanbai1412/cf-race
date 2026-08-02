import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(2229)
w = Writer(sys.argv[1])


def case(a):
    return f"{len(a)}\n{' '.join(map(str, a))}"


def rand_cases(tcnt, total_n, lo=1, hi=1000):
    cases, left = [], total_n
    for i in range(tcnt):
        n = left - 2 * (tcnt - 1 - i) if i == tcnt - 1 else rng.randint(2, max(2, left - 2 * (tcnt - 1 - i)))
        n = max(2, min(n, left - 2 * (tcnt - 1 - i)))
        left -= n
        cases.append(case([rng.randint(lo, hi) for _ in range(n)]))
    return multi(cases)


# edges
w.add(multi([case([1, 1]), case([1, 1000]), case([1000, 1]), case([500, 500])]))
w.add(multi([case([1] * 2 + [1000]), case(list(range(1, 21)))]))
# all equal / two distinct values
w.add(multi([case([7] * 100), case([1, 2] * 50), case([1, 1000] * 50)]))

# small exhaustive pairs
w.add(multi([case([a, b]) for a in range(1, 11) for b in range(1, 11)]))

# randoms
for _ in range(10):
    w.add(rand_cases(rng.randint(2, 50), rng.randint(100, 900)))
for lo, hi in ((1, 10), (990, 1000), (1, 2)):
    w.add(rand_cases(20, 500, lo, hi))

# max-size: t=100, sum n = 1000
w.add(rand_cases(100, 1000))
w.add(multi([case([rng.randint(1, 1000) for _ in range(1000 - 2 * 0)])][:1]))
w.add(multi([case([1] + [1000] * 999)]))
