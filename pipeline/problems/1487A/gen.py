import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1487)
    w = Writer(outdir)

    # edge cases
    w.add(multi([
        case([1, 1]),                  # all equal, minimum n
        case([1, 2]),
        case([100, 100]),
        case([1] * 100),               # all equal, max n
        case([1] * 99 + [2]),          # single winner
        case([1] + [100] * 99),        # 99 winners
        case(list(range(1, 101))),     # all distinct, max n
        case([100] * 50 + [1] * 50),
        case([3, 2, 2]),
        case([1, 3, 3, 7]),
    ]))

    # small random tests
    for _ in range(5):
        cases = []
        for _ in range(rnd.randint(1, 100)):
            n = rnd.randint(2, 6)
            cases.append(case([rnd.randint(1, 5) for _ in range(n)]))
        w.add(multi(cases))

    # random tests over the full range
    for _ in range(3):
        cases = []
        for _ in range(rnd.randint(100, 500)):
            n = rnd.randint(2, 100)
            cases.append(case([rnd.randint(1, 100) for _ in range(n)]))
        w.add(multi(cases))

    # max size: t = 500, n = 100
    w.add(multi([case([rnd.randint(1, 3) for _ in range(100)]) for _ in range(500)]))


if __name__ == "__main__":
    main(sys.argv[1])
