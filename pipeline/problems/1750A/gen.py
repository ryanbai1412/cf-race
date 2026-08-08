import itertools
import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1750)
    w = Writer(outdir)
    # exhaustive: all permutations of size 3 and 4
    small = [case(p) for p in itertools.permutations(range(1, 4))]
    small += [case(p) for p in itertools.permutations(range(1, 5))]
    w.add(multi(small))
    # edges: sorted, reversed, 1 first / 1 last at n=10
    w.add(multi([case(list(range(1, 11))), case(list(range(10, 0, -1))),
                 case([1] + list(range(10, 1, -1))),
                 case(list(range(2, 11)) + [1])]))
    # max t=5000 random
    def rp():
        n = rnd.randint(3, 10)
        p = list(range(1, n + 1))
        rnd.shuffle(p)
        return case(p)
    w.add(multi([rp() for _ in range(5000)]))
    for _ in range(5):
        w.add(multi([rp() for _ in range(rnd.randint(1, 100))]))


if __name__ == "__main__":
    main(sys.argv[1])
