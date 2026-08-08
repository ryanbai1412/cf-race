import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

M = 10**8


def case(a, b, c, x, y):
    return f"{a} {b} {c} {x} {y}"


def main(outdir):
    rnd = random.Random(1675)
    w = Writer(outdir)
    # edge cases: zeros, maxima, exact boundaries
    edge = [
        case(0, 0, 0, 0, 0),
        case(0, 0, 0, 1, 0),
        case(0, 0, 0, 0, 1),
        case(M, M, M, M, M),
        case(0, 0, M, M // 2, M - M // 2),
        case(0, 0, M, M // 2, M - M // 2 + 1),
        case(M, 0, 0, M, 0),
        case(0, M, 0, 0, M),
        case(1, 1, 1, 2, 2),
        case(1, 1, 2, 2, 2),
        case(0, 0, M, M, 0),
        case(0, 0, M, 0, M),
        case(M, M, 0, 0, 0),
    ]
    w.add(multi(edge))
    # small random (boundary-heavy)
    for _ in range(4):
        cs = []
        for _ in range(200):
            cs.append(case(*(rnd.randint(0, 10) for _ in range(5))))
        w.add(multi(cs))
    # large random
    for _ in range(4):
        cs = []
        for _ in range(1000):
            cs.append(case(*(rnd.randint(0, M) for _ in range(5))))
        w.add(multi(cs))
    # max t with near-boundary answers
    cs = []
    for _ in range(10000):
        x = rnd.randint(0, M)
        y = rnd.randint(0, M)
        a = rnd.randint(max(0, x - 100), x) if x else 0
        b = rnd.randint(max(0, y - 100), y) if y else 0
        c = max(0, x - a) + max(0, y - b) + rnd.randint(-2, 2)
        c = min(max(c, 0), M)
        cs.append(case(a, b, c, x, y))
    w.add(multi(cs))


if __name__ == "__main__":
    main(sys.argv[1])
