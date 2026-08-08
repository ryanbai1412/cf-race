import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(b, p, f, h, c):
    return f"{b} {p} {f}\n{h} {c}"


def rcase(rnd, hi=100):
    return case(rnd.randint(1, hi), rnd.randint(1, hi), rnd.randint(1, hi),
                rnd.randint(1, hi), rnd.randint(1, hi))


def main(outdir):
    rnd = random.Random(1207)
    w = Writer(outdir)
    # edges: one bun (no burgers), equal prices, maximal everything
    w.add(multi([case(1, 100, 100, 100, 100),
                 case(100, 100, 100, 100, 100),
                 case(100, 100, 100, 50, 50),
                 case(2, 1, 1, 100, 99),
                 case(2, 1, 1, 99, 100),
                 case(1, 1, 1, 1, 1),
                 case(100, 1, 1, 100, 100),
                 case(3, 100, 100, 7, 9)]))
    # small randoms
    for _ in range(6):
        w.add(multi([rcase(rnd, 5) for _ in range(rnd.randint(1, 30))]))
    # full randoms, max t
    for _ in range(4):
        w.add(multi([rcase(rnd) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
