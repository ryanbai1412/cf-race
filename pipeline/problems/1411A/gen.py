import random
import string
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer, multi

rng = random.Random(1411)
w = Writer(sys.argv[1])
LETTERS = string.ascii_lowercase


def case(s):
    return f"{len(s)}\n{s}"


def rand_str(n, p=0.5):
    return "".join(")" if rng.random() < p else rng.choice(LETTERS)
                   for _ in range(n))


def tail_case(n, k):
    head = "".join(rng.choice(LETTERS + ")") for _ in range(n - k))
    if head.endswith(")"):
        head = head[:-1] + rng.choice(LETTERS)
    return case(head + ")" * k)


# edges
w.add(multi([case(")"), case("a"), case("))"), case("a)"), case(")a"),
             case(")" * 100), case("a" * 100), case("a" * 50 + ")" * 50),
             case("a" * 51 + ")" * 49), case("a" * 49 + ")" * 51),
             case(")bc)))")]))
# boundary tails around n/2
for n in (1, 2, 3, 99, 100):
    w.add(multi([tail_case(n, k) for k in range(1, n + 1)][:100]))
# random densities
for p in (0.1, 0.3, 0.5, 0.7, 0.9):
    w.add(multi([rand_str(rng.randint(1, 100), p) for _ in range(100)]
                and [case(rand_str(rng.randint(1, 100), p))
                     for _ in range(100)]))
# random tails, max size t=100 n=100
for _ in range(3):
    w.add(multi([tail_case(100, rng.randint(1, 100)) for _ in range(100)]))
w.add(multi([tail_case(100, 50) for _ in range(100)]))
w.add(multi([tail_case(100, 51) for _ in range(100)]))
