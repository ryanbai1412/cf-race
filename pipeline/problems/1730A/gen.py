import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, c, a):
    return f"{n} {c}\n" + " ".join(map(str, a))


def rand_case(rnd, max_n=100, max_c=100, max_a=100):
    n = rnd.randint(1, max_n)
    c = rnd.randint(1, max_c)
    a = [rnd.randint(1, max_a) for _ in range(n)]
    return case(n, c, a)


def main(outdir):
    rnd = random.Random(1730)
    w = Writer(outdir)
    # edges: n=1, c=1 (never batch), c=100 (batch rarely pays), all same orbit
    w.add(multi([case(1, 1, [1]), case(1, 100, [100]),
                 case(100, 1, [50] * 100), case(100, 100, [7] * 100),
                 case(100, 2, list(range(1, 101))),
                 case(100, 100, list(range(1, 101))),
                 case(100, 50, [1] * 50 + [2] * 50)]))
    # random with small orbit range (many duplicates)
    w.add(multi([rand_case(rnd, max_a=5) for _ in range(100)]))
    w.add(multi([rand_case(rnd, max_a=10, max_c=3) for _ in range(100)]))
    # fully random, max t
    w.add(multi([rand_case(rnd) for _ in range(100)]))
    w.add(multi([rand_case(rnd, max_c=5) for _ in range(100)]))
    # max size everything
    w.add(multi([case(100, rnd.randint(1, 100),
                      [rnd.randint(1, 100) for _ in range(100)])
                 for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
