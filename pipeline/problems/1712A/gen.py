import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, k, p):
    return f"{n} {k}\n" + " ".join(map(str, p))


def rand_case(rnd, nmax=100):
    n = rnd.randint(1, nmax)
    k = rnd.randint(1, n)
    p = list(range(1, n + 1))
    rnd.shuffle(p)
    return case(n, k, p)


def main(outdir):
    rnd = random.Random(1712)
    w = Writer(outdir)
    # edge: n=1, k=n (always 0), identity, reversed
    w.add(multi([case(1, 1, [1]), case(5, 5, [3, 1, 5, 2, 4]),
                 case(5, 2, [1, 2, 3, 4, 5]),
                 case(5, 2, [5, 4, 3, 2, 1]),
                 case(4, 2, [3, 4, 1, 2])]))
    # random small
    for _ in range(3):
        w.add(multi([rand_case(rnd, 8) for _ in range(100)]))
    # random mixed
    for _ in range(3):
        w.add(multi([rand_case(rnd, 50) for _ in range(100)]))
    # max size
    w.add(multi([rand_case(rnd, 100) for _ in range(100)]))
    w.add(multi([case(100, rnd.randint(1, 100), rnd.sample(range(1, 101), 100))
                 for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
