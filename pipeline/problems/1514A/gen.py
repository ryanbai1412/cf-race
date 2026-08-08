import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

SQUARES = [i * i for i in range(1, 101)]  # squares <= 10^4


def case(rnd, n, all_squares=False, one_nonsquare=False):
    if all_squares:
        a = [rnd.choice(SQUARES) for _ in range(n)]
    elif one_nonsquare:
        a = [rnd.choice(SQUARES) for _ in range(n)]
        a[rnd.randrange(n)] = rnd.choice([x for x in range(2, 10001) if int(x**0.5) ** 2 != x])
    else:
        a = [rnd.randint(1, 10000) for _ in range(n)]
    return f"{n}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1514)
    w = Writer(outdir)
    # single-element edges
    w.add(multi(["1\n1", "1\n2", "1\n10000", "1\n9999", "1\n4"]))
    # all squares (NO answers)
    w.add(multi([case(rnd, rnd.randint(1, 100), all_squares=True) for _ in range(100)]))
    # exactly one non-square hidden among squares
    w.add(multi([case(rnd, rnd.randint(1, 100), one_nonsquare=True) for _ in range(100)]))
    # random
    for _ in range(3):
        w.add(multi([case(rnd, rnd.randint(1, 100)) for _ in range(100)]))
    # max size mixed
    w.add(multi([case(rnd, 100, all_squares=(i % 2 == 0)) for i in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
