import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402


def case(rnd, ones, zeros):
    letters = list("one" * ones + "zero" * zeros)
    rnd.shuffle(letters)
    return f"{len(letters)}\n{''.join(letters)}\n"


def main(outdir):
    rnd = random.Random(1220)
    w = Writer(outdir)
    w.add(case(rnd, 1, 0))
    w.add(case(rnd, 0, 1))
    w.add(case(rnd, 5, 0))
    w.add(case(rnd, 0, 5))
    w.add(case(rnd, 1, 1))
    # small randoms
    for _ in range(6):
        w.add(case(rnd, rnd.randint(0, 8), rnd.randint(0, 8)))
    # larger randoms
    for _ in range(4):
        w.add(case(rnd, rnd.randint(0, 500), rnd.randint(0, 500)))
    # max-size: n = 1e5 (25000 zeros / mixed)
    w.add(case(rnd, 0, 25000))
    w.add(case(rnd, 33333, 0)[:0] or case(rnd, 33332, 1))
    w.add(case(rnd, 20000, 10000))


if __name__ == "__main__":
    main(sys.argv[1])
