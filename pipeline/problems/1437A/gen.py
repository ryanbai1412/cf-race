import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXV = 10 ** 9


def case(l, r):
    return f"{l} {r}"


def main(outdir):
    rnd = random.Random(1437)
    w = Writer(outdir)

    # edges: l == r, r == 2l (NO), r == 2l-1 (YES), extreme values
    w.add(multi([
        case(1, 1),
        case(1, 2),
        case(2, 3),
        case(2, 4),
        case(MAXV, MAXV),
        case(1, MAXV),
        case(MAXV // 2, MAXV),
        case(MAXV // 2 + 1, MAXV),
        case(499999999, 999999999),
        case(500000000, 999999999),
    ]))

    # max t with boundary-heavy cases
    cases = []
    for _ in range(1000):
        l = rnd.randint(1, MAXV // 2)
        r = rnd.choice([2 * l - 1, 2 * l, 2 * l + 1, l])
        cases.append(case(l, min(r, MAXV)))
    w.add(multi(cases))

    # max t fully random
    cases = []
    for _ in range(1000):
        l = rnd.randint(1, MAXV)
        r = rnd.randint(l, MAXV)
        cases.append(case(l, r))
    w.add(multi(cases))

    # small exhaustive-ish ranges
    cases = [case(l, r) for l in range(1, 8) for r in range(l, 12)]
    w.add(multi(cases))

    for _ in range(10):
        t = rnd.randint(1, 50)
        cases = []
        for _ in range(t):
            l = rnd.randint(1, 30)
            r = rnd.randint(l, 60)
            cases.append(case(l, r))
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
