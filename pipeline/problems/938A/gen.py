import random
import string
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer

VOWELS = "aeiouy"
CONS = "".join(c for c in string.ascii_lowercase if c not in VOWELS)
MAXN = 100
rng = random.Random(9381)
w = Writer(sys.argv[1])


def case(s):
    return f"{len(s)}\n{s}"


# edges
w.add(case("a"))
w.add(case("b"))
w.add(case("y"))
w.add(case("aa"))
w.add(case("ay"))
w.add(case("ya"))
w.add(case("ab"))
w.add(case("a" * MAXN))
w.add(case("aeiouy" * 16 + "aeiu"))
w.add(case(("ab" * 50)))
w.add(case(("ba" * 50)))
w.add(case("".join(rng.choice(CONS) for _ in range(MAXN))))
w.add(case("aab" + "e" * 50 + "z" + "iou" * 15))

# randoms with different vowel densities
for p in (0.1, 0.3, 0.5, 0.7, 0.9):
    for _ in range(2):
        n = rng.randint(1, MAXN)
        s = "".join(rng.choice(VOWELS) if rng.random() < p else rng.choice(CONS)
                    for _ in range(n))
        w.add(case(s))
