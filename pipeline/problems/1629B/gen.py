import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MX = 10**9


def case(l, r, k):
    return f"{l} {r} {k}"


def rand_case(rnd, lo, hi):
    l = rnd.randint(lo, hi)
    r = rnd.randint(l, hi)
    return case(l, r, rnd.randint(0, r - l))


def main(outdir):
    rnd = random.Random(16292)
    w = Writer(outdir)

    # edges: single element (1, prime, composite), max range, boundary k
    w.add(
        multi(
            [
                case(1, 1, 0),
                case(2, 2, 0),
                case(1, MX, MX - 1),
                case(1, MX, MX // 2 - 1),
                case(1, MX, MX // 2),
                case(MX, MX, 0),
                case(MX - 1, MX, 0),
                case(MX - 1, MX, 1),
                case(2, 3, 1),
                case(999999937, 999999937, 0),
            ]
        )
    )

    # small ranges (brute-force verifiable region)
    for _ in range(3):
        w.add(multi([rand_case(rnd, 1, 30) for _ in range(10**4)]))
    w.add(multi([rand_case(rnd, 1, 1000) for _ in range(2 * 10**4)]))

    # k near the odds-count boundary
    cases = []
    for _ in range(3 * 10**4):
        l = rnd.randint(1, MX)
        r = rnd.randint(l, min(MX, l + rnd.choice([0, 1, 2, 10, 10**6])))
        odds = (r + 1) // 2 - l // 2
        k = max(0, min(r - l, odds + rnd.randint(-1, 1)))
        cases.append(case(l, r, k))
    w.add(multi(cases))

    # max t, full range
    w.add(multi([rand_case(rnd, 1, MX) for _ in range(3 * 10**4)]))


if __name__ == "__main__":
    main(sys.argv[1])
