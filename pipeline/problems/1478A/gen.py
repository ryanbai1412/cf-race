import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


def sorted_case(a):
    return case(sorted(a))


def main(outdir):
    rnd = random.Random(1478)
    w = Writer(outdir)

    # edge cases
    w.add(multi([
        case([1]),                       # n = 1
        case([1, 1]),                    # all equal, n = 2
        case([1, 2]),                    # strictly increasing
        case([100] * 100),               # max repetition
        case(list(range(1, 101))),       # all distinct, max n
        case([1] * 50 + [2] * 50),
        case([1] * 99 + [100]),
        case(sorted([1] * 3 + [2] * 7 + [3] * 5)),
    ]))

    # small random tests
    for _ in range(4):
        cases = []
        for _ in range(rnd.randint(1, 100)):
            n = rnd.randint(1, 8)
            cases.append(sorted_case([rnd.randint(1, n) for _ in range(n)]))
        w.add(multi(cases))

    # random tests over the full range
    for _ in range(4):
        cases = []
        for _ in range(rnd.randint(50, 100)):
            n = rnd.randint(1, 100)
            cases.append(sorted_case([rnd.randint(1, n) for _ in range(n)]))
        w.add(multi(cases))

    # max size: t = 100, n = 100
    w.add(multi([sorted_case([rnd.randint(1, 100) for _ in range(100)]) for _ in range(100)]))
    # few distinct values -> large answers
    w.add(multi([sorted_case([rnd.randint(1, k) for _ in range(100)])
                 for k in range(1, 11) for _ in range(10)]))


if __name__ == "__main__":
    main(sys.argv[1])
