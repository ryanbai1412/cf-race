import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1490)
    w = Writer(outdir)

    # edge cases
    w.add(multi([
        case([1, 1]),                     # minimum n, already dense
        case([1, 50]),                    # worst single pair
        case([50, 1]),
        case([1, 2]),                     # exactly ratio 2
        case([1, 3]),                     # just over ratio 2
        case([50] * 50),                  # max n, all equal
        case([1, 50] * 25),               # max n, alternating extremes
        case([4, 2, 10, 1]),
        case(list(range(1, 51))),
        case(list(range(50, 0, -1))),
    ]))

    # small random tests
    for _ in range(5):
        cases = []
        for _ in range(rnd.randint(1, 100)):
            n = rnd.randint(2, 5)
            cases.append(case([rnd.randint(1, 20) for _ in range(n)]))
        w.add(multi(cases))

    # random tests over the full range
    for _ in range(3):
        cases = []
        for _ in range(rnd.randint(100, 1000)):
            n = rnd.randint(2, 50)
            cases.append(case([rnd.randint(1, 50) for _ in range(n)]))
        w.add(multi(cases))

    # max size: t = 1000, n = 50, extreme jumps
    w.add(multi([case([rnd.choice([1, 2, 49, 50]) for _ in range(50)]) for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
