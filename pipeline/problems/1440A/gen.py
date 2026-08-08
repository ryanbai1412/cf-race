import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXV = 1000


def case(n, c0, c1, h, s):
    return f"{n} {c0} {c1} {h}\n{s}"


def main(outdir):
    rnd = random.Random(1440)
    w = Writer(outdir)

    # edges: n=1, all zeros/ones, h exactly the break-even point, max values
    w.add(multi([
        case(1, 1, 1, 1, "0"),
        case(1, 1, 1, 1, "1"),
        case(1, 1000, 1, 1000, "0"),
        case(1, 1, 1000, 1000, "1"),
        case(2, 5, 3, 2, "00"),
        case(2, 5, 3, 1, "00"),
        case(3, 3, 5, 2, "111"),
        case(3, 3, 5, 1, "111"),
        case(4, 1000, 1000, 1000, "0101"),
        case(5, 1, 1000, 1, "11111"),
    ][:10]))

    # max-size: t=10 with n=1000 random strings
    for _ in range(4):
        cases = []
        for _ in range(10):
            n = MAXV
            s = "".join(rnd.choice("01") for _ in range(n))
            cases.append(case(n, rnd.randint(1, MAXV), rnd.randint(1, MAXV),
                              rnd.randint(1, MAXV), s))
        w.add(multi(cases))

    # max-size all-zero / all-one strings with extreme costs
    w.add(multi([
        case(MAXV, 1000, 1, 1, "0" * MAXV),
        case(MAXV, 1, 1000, 1, "1" * MAXV),
        case(MAXV, 1000, 1, 1000, "0" * MAXV),
        case(MAXV, 1, 1000, 1000, "1" * MAXV),
        case(MAXV, 500, 500, 1, "01" * (MAXV // 2)),
    ]))

    # random small cases
    for _ in range(9):
        cases = []
        for _ in range(rnd.randint(1, 10)):
            n = rnd.randint(1, 12)
            s = "".join(rnd.choice("01") for _ in range(n))
            cases.append(case(n, rnd.randint(1, 20), rnd.randint(1, 20),
                              rnd.randint(1, 20), s))
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
