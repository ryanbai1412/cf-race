import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAX = 10**9


def case(n, k, a):
    return f"{n} {k}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1430)
    w = Writer(outdir)
    # edge cases
    w.add(multi([
        case(2, 1, [0, 0]),
        case(2, 1, [MAX, MAX]),
        case(2, 1, [0, MAX]),
        case(3, 2, [MAX, MAX, MAX]),
        case(4, 1, [5, 5, 5, 5]),
    ]))
    # all zeros / all max, various k
    w.add(multi([case(10, k, [0] * 10) for k in range(1, 10)]))
    w.add(multi([case(10, k, [MAX] * 10) for k in range(1, 10)]))
    # small random, many cases
    for _ in range(3):
        cases = []
        for _ in range(200):
            n = rnd.randint(2, 10)
            k = rnd.randint(1, n - 1)
            cases.append(case(n, k, [rnd.randint(0, 20) for _ in range(n)]))
        w.add(multi(cases))
    # large tests (n capped so each input stays < 1MB)
    n = 80000
    w.add(multi([case(n, n - 1, [rnd.randint(0, MAX) for _ in range(n)])]))
    w.add(multi([case(n, 1, [rnd.randint(0, MAX) for _ in range(n)])]))
    w.add(multi([case(n, rnd.randint(1, n - 1), [MAX] * n)]))
    # many mid-size cases in one input
    cases = []
    for _ in range(1000):
        n = 80
        k = rnd.randint(1, n - 1)
        cases.append(case(n, k, [rnd.randint(0, MAX) for _ in range(n)]))
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
