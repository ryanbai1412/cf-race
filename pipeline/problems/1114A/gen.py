import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402

M = 10**5


def case(x, y, z, a, b, c):
    return f"{x} {y} {z}\n{a} {b} {c}\n"


def main(outdir):
    rnd = random.Random(1114)
    w = Writer(outdir)
    # extremes
    w.add(case(1, 1, 1, 1, 1, 1))
    w.add(case(M, M, M, M, M, M))
    w.add(case(1, 1, 1, M, M, M))
    w.add(case(M, M, M, 1, 1, 1))
    # exact fit: a=x, a-x+b=y, total=x+y+z
    w.add(case(10, 20, 30, 10, 20, 30))
    # green enough but purple short by one
    w.add(case(5, 10, 1, 5, 4, 1))
    # everything hinges on last grape
    w.add(case(M, M, M, M, M, M - 1))
    w.add(case(1, 1, M, 1, 1, M - 2))
    # small randoms (both verdicts likely)
    for _ in range(6):
        x, y, z = (rnd.randint(1, 6) for _ in range(3))
        a, b, c = (rnd.randint(1, 6) for _ in range(3))
        w.add(case(x, y, z, a, b, c))
    # large randoms
    for _ in range(4):
        x, y, z = (rnd.randint(1, M) for _ in range(3))
        a, b, c = (rnd.randint(1, M) for _ in range(3))
        w.add(case(x, y, z, a, b, c))


if __name__ == "__main__":
    main(sys.argv[1])
