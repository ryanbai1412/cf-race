import random
import string
import sys

sys.path.insert(0, __file__.rsplit("/", 3)[0])
from genlib import Writer

rng = random.Random(1539)
w = Writer(sys.argv[1])


def case(s: str, queries) -> str:
    lines = [f"{len(s)} {len(queries)}", s]
    lines += [f"{l} {r}" for l, r in queries]
    return "\n".join(lines) + "\n"


def rand_queries(n, q):
    out = []
    for _ in range(q):
        l = rng.randint(1, n)
        r = rng.randint(l, n)
        out.append((l, r))
    return out


# edge: minimal
w.add(case("a", [(1, 1)]))
w.add(case("z", [(1, 1)]))
# all z, single char queries
w.add(case("z" * 10, [(i, j) for i in range(1, 11) for j in range(i, 11)]))
# small random alphabets
for n in (2, 5, 17, 100):
    s = "".join(rng.choice(string.ascii_lowercase) for _ in range(n))
    w.add(case(s, rand_queries(n, min(200, n * n))))

# medium
for n in (1000, 10000):
    s = "".join(rng.choice(string.ascii_lowercase) for _ in range(n))
    w.add(case(s, rand_queries(n, 5000)))

# max n, all 'z' (max answers), full-range queries
n = 100000
w.add(case("z" * n, [(1, n)] * 1000 + rand_queries(n, 20000)))

# max n with random letters, many queries (kept under ~1MB)
for _ in range(3):
    s = "".join(rng.choice(string.ascii_lowercase) for _ in range(n))
    w.add(case(s, rand_queries(n, 60000)))

# max n, only one letter kind but sparse queries; plus max-length single query
s = "".join(rng.choice("az") for _ in range(n))
w.add(case(s, [(1, n), (n, n), (1, 1)] + rand_queries(n, 60000)))
