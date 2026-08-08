import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

M = 10 ** 9


def case(r, b, d):
    return f"{r} {b} {d}"


def main(outdir):
    rnd = random.Random(1519)
    w = Writer(outdir)
    # edges
    w.add(multi([case(1, 1, 0), case(M, M, 0), case(M, 1, M),
                 case(1, M, M - 2), case(1, M, M - 1), case(M, 1, 0),
                 case(1, 1, M)]))
    # exact boundary hi == lo*(d+1) and +-1
    cases = []
    for lo in (1, 2, 3, 1000, 31623):
        for d in (0, 1, 2, 1000):
            hi = lo * (d + 1)
            for delta in (-1, 0, 1):
                if 1 <= hi + delta <= M:
                    cases.append(case(hi + delta, lo, d))
                    cases.append(case(lo, hi + delta, d))
    w.add(multi(cases[:1000]))
    # max size random
    for seed in range(3):
        cases = []
        for _ in range(1000):
            if rnd.random() < 0.5:
                r, b = rnd.randint(1, M), rnd.randint(1, M)
                d = rnd.randint(0, M)
            else:
                lo = rnd.randint(1, 1000)
                d = rnd.randint(0, 1000)
                r, b = lo, min(M, lo * (d + 1) + rnd.randint(-2, 2))
                if b < 1:
                    b = 1
                if rnd.random() < 0.5:
                    r, b = b, r
            cases.append(case(r, b, d))
        w.add(multi(cases))
    # small exhaustive-ish
    w.add(multi([case(r, b, d) for r in range(1, 7) for b in range(1, 7)
                 for d in range(0, 4)][:1000]))


if __name__ == "__main__":
    main(sys.argv[1])
