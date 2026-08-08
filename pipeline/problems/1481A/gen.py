import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(px, py, s):
    return f"{px} {py}\n{s}"


def main(outdir):
    rnd = random.Random(1481)
    w = Writer(outdir)

    # edge cases
    w.add(multi([
        case(1, 0, "R"),
        case(-1, 0, "R"),
        case(0, 1, "U"),
        case(0, -1, "D"),
        case(1, 1, "RU"),
        case(1, 1, "UR"),
        case(2, 0, "R"),                       # not enough R
        case(10 ** 5, 0, "R" * 10 ** 5),       # exact fit, max coordinate
        case(-10 ** 5, 0, "L" * 10 ** 5),
        case(10 ** 5, 1, "R" * 10 ** 5),       # missing one U
    ]))

    # small random tests
    for _ in range(5):
        cases = []
        for _ in range(rnd.randint(1, 60)):
            s = "".join(rnd.choice("UDLR") for _ in range(rnd.randint(1, 8)))
            px = rnd.randint(-4, 4)
            py = rnd.randint(-4, 4)
            if (px, py) == (0, 0):
                px = 1
            cases.append(case(px, py, s))
        w.add(multi(cases))

    # medium random tests
    for _ in range(3):
        cases = []
        for _ in range(rnd.randint(50, 500)):
            s = "".join(rnd.choice("UDLR") for _ in range(rnd.randint(1, 100)))
            px = rnd.randint(-60, 60)
            py = rnd.randint(-60, 60)
            if (px, py) == (0, 0):
                px = -1
            cases.append(case(px, py, s))
        w.add(multi(cases))

    # max t = 1000 with total |s| = 1e5
    cases = []
    for _ in range(1000):
        s = "".join(rnd.choice("UDLR") for _ in range(100))
        px = rnd.randint(-30, 30)
        py = rnd.randint(-30, 30)
        if (px, py) == (0, 0):
            py = 30
        cases.append(case(px, py, s))
    w.add(multi(cases))

    # one huge string, skewed alphabet
    s = "".join(rnd.choice("UUUR") for _ in range(10 ** 5))
    w.add(multi([case(s.count("R"), s.count("U"), s),
                 case(s.count("R") + 1, s.count("U"), s)]))


if __name__ == "__main__":
    main(sys.argv[1])
