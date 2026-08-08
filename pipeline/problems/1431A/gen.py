import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAX = 10**12


def case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1431)
    w = Writer(outdir)
    # edges
    w.add(multi([
        case([1]),
        case([MAX]),
        case([1] * 100),
        case([MAX] * 100),
        case(list(range(1, 101))),
        case([MAX - i for i in range(100)]),
    ]))
    # small random values
    for _ in range(3):
        cases = []
        for _ in range(100):
            n = rnd.randint(1, 10)
            cases.append(case([rnd.randint(1, 20) for _ in range(n)]))
        w.add(multi(cases))
    # large random values, max size (t=100, n=100)
    for _ in range(4):
        cases = []
        for _ in range(100):
            cases.append(case([rnd.randint(1, MAX) for _ in range(100)]))
        w.add(multi(cases))
    # skewed distributions (few big, many small)
    cases = []
    for _ in range(100):
        n = rnd.randint(2, 100)
        big = rnd.randint(MAX // 2, MAX)
        arr = [rnd.randint(1, 1000) for _ in range(n - 1)] + [big]
        rnd.shuffle(arr)
        cases.append(case(arr))
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
