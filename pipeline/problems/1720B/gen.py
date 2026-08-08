import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MV = 10**9


def case(a):
    return f"{len(a)}\n{' '.join(map(str, a))}"


def main(outdir):
    rnd = random.Random(1720)
    w = Writer(outdir)
    # edge patterns at n=4
    w.add(multi([
        case([1, 1, 1, 1]),
        case([MV, MV, MV, MV]),
        case([1, MV, 1, MV]),
        case([MV, 1, 1, MV]),
        case([1, 2, 3, 4]),
        case([4, 3, 2, 1]),
    ]))
    # extremes at ends vs middle
    w.add(multi([
        case([MV, 1, 5, 1, MV]),
        case([1, MV, MV, 1, 5]),
        case([5, 5, 5, 5, 5, 1]),
    ]))
    # small random cases
    for _ in range(4):
        cases = []
        for _ in range(200):
            n = rnd.randint(4, 12)
            cases.append(case([rnd.randint(1, 100) for _ in range(n)]))
        w.add(multi(cases))
    # large random values
    cases = []
    for _ in range(100):
        n = rnd.randint(4, 500)
        cases.append(case([rnd.randint(1, MV) for _ in range(n)]))
    w.add(multi(cases))
    # max-size test: one array of n = 1e5
    w.add(multi([case([rnd.randint(1, MV) for _ in range(10**5)])]))
    # max-size split across many cases
    cases = []
    rem = 10**5
    while rem >= 4:
        n = min(rnd.randint(4, 200), rem)
        cases.append(case([rnd.randint(1, MV) for _ in range(n)]))
        rem -= n
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
