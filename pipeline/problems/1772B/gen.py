import itertools
import random
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(17721)
w = Writer(sys.argv[1])


def case(m):
    return f"{m[0]} {m[1]}\n{m[2]} {m[3]}"


def rand_case(lo=1, hi=100):
    return rng.sample(range(lo, hi + 1), 4)


# exhaustive over all 24 permutations of {1,2,3,4}
w.add(multi([case(list(p)) for p in itertools.permutations([1, 2, 3, 4])]))
# exhaustive over all permutations of the extreme values
w.add(multi([case(list(p)) for p in itertools.permutations([1, 2, 99, 100])]))
# edges
w.add(multi([
    case([1, 2, 3, 4]), case([4, 3, 2, 1]), case([1, 100, 2, 99]),
    case([100, 1, 99, 2]), case([1, 3, 2, 4]), case([2, 4, 1, 3]),
]))
# random over all four elements small range
for hi in (4, 6, 10, 100):
    for _ in range(3):
        w.add(multi([case(rand_case(1, hi)) for _ in range(rng.randint(50, 500))]))
# max size t = 1000
for _ in range(3):
    w.add(multi([case(rand_case()) for _ in range(1000)]))
w.add(multi([case(list(itertools.permutations([1, 2, 3, 4])[0] if False else rand_case(1, 4)))
             for _ in range(1000)]))
