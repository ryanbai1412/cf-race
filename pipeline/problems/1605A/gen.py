import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a, b, c):
    return f"{a} {b} {c}"


def main(outdir):
    rnd = random.Random(1605)
    w = Writer(outdir)
    # edge: minimal and maximal values, all residues mod 3
    w.add(multi([
        case(1, 1, 1),
        case(1, 1, 2),
        case(1, 2, 2),
        case(10**8, 10**8, 10**8),
        case(10**8, 10**8, 10**8 - 1),
        case(10**8, 10**8 - 1, 10**8 - 2),
        case(1, 1, 10**8),
    ]))
    # random small
    for _ in range(4):
        w.add(multi([
            case(rnd.randint(1, 9), rnd.randint(1, 9), rnd.randint(1, 9))
            for _ in range(1000)
        ]))
    # random large
    for _ in range(3):
        w.add(multi([
            case(rnd.randint(1, 10**8), rnd.randint(1, 10**8), rnd.randint(1, 10**8))
            for _ in range(1000)
        ]))
    # max-size: t = 5000
    w.add(multi([
        case(rnd.randint(1, 10**8), rnd.randint(1, 10**8), rnd.randint(1, 10**8))
        for _ in range(5000)
    ]))


if __name__ == "__main__":
    main(sys.argv[1])
