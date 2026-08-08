import random
import string
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1703 * 2)
w = Writer(sys.argv[1])


def case(s):
    return f"{len(s)}\n{s}"


def rand_s(n, alpha):
    return "".join(rng.choice(alpha) for _ in range(n))


# edge: single letter, all same, all distinct
w.add(multi([case("A"), case("Z"), case("A" * 50), case(string.ascii_uppercase * 1)[:0] or case(string.ascii_uppercase[:26])]))
# all distinct max, all same max, two letters
w.add(multi([case(string.ascii_uppercase + string.ascii_uppercase[:24]),
             case("Q" * 50), case("ABAB" * 12)]))
# random with varying alphabet sizes, max t
for k in (1, 2, 3, 5, 26):
    w.add(multi([case(rand_s(rng.randint(1, 50), string.ascii_uppercase[:k])) for _ in range(100)]))
# fully random max t max n
for _ in range(2):
    w.add(multi([case(rand_s(50, string.ascii_uppercase)) for _ in range(100)]))
