import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXA = 10 ** 6


def case(n, m, a):
    return f"{n} {m}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1436)
    w = Writer(outdir)

    # edges: n=1, zeros, m=0, m at the bound, sums just off by one
    w.add(multi([
        case(1, 0, [0]),
        case(1, 1, [1]),
        case(1, MAXA, [MAXA]),
        case(1, 0, [1]),
        case(2, 0, [0, 0]),
        case(3, 0, [0, 0, 1]),
    ]))

    # max-size cases: n=100 with max values (sum far above m bound => NO)
    w.add(multi([case(100, MAXA, [MAXA] * 100) for _ in range(100)]))

    # n=100 arrays whose sum is exactly m (all YES)
    cases = []
    for _ in range(100):
        n = 100
        a = [rnd.randint(0, MAXA // n) for _ in range(n)]
        cases.append(case(n, sum(a), a))
    w.add(multi(cases))

    # random mix of YES/NO with small values
    for _ in range(12):
        t = rnd.randint(1, 100)
        cases = []
        for _ in range(t):
            n = rnd.randint(1, 10)
            a = [rnd.randint(0, 10) for _ in range(n)]
            s = sum(a)
            m = s if rnd.random() < 0.5 else max(0, s + rnd.randint(-2, 2))
            cases.append(case(n, m, a))
        w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
