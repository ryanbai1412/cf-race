import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a, b, c):
    return f"{a} {b} {c}"


def main(outdir):
    rnd = random.Random(1593)
    w = Writer(outdir)
    # edge: zeros and ties
    w.add(multi([
        case(0, 0, 0),
        case(1, 1, 1),
        case(0, 0, 1),
        case(0, 1, 0),
        case(1, 0, 0),
        case(5, 5, 3),
        case(5, 3, 5),
        case(3, 5, 5),
        case(10**9, 10**9, 10**9),
        case(10**9, 0, 0),
        case(0, 10**9, 10**9),
    ]))
    # random small (ties frequent)
    for _ in range(4):
        w.add(multi([
            case(rnd.randint(0, 4), rnd.randint(0, 4), rnd.randint(0, 4))
            for _ in range(500)
        ]))
    # random large
    for _ in range(3):
        w.add(multi([
            case(rnd.randint(0, 10**9), rnd.randint(0, 10**9), rnd.randint(0, 10**9))
            for _ in range(1000)
        ]))
    # max-size: t = 10^4
    w.add(multi([
        case(rnd.randint(0, 10**9), rnd.randint(0, 10**9), rnd.randint(0, 10**9))
        for _ in range(10**4)
    ]))


if __name__ == "__main__":
    main(sys.argv[1])
