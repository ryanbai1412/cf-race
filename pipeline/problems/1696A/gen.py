import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAX = (1 << 30) - 1


def case(z, a):
    return f"{len(a)} {z}\n{' '.join(map(str, a))}"


def main(outdir):
    rnd = random.Random(16961)
    w = Writer(outdir)
    # edge cases
    edge = [
        case(0, [0]),
        case(MAX, [0]),
        case(0, [MAX]),
        case(MAX, [MAX]),
        case(rnd.randint(0, MAX), [rnd.randint(0, MAX)]),
        case(5, [1, 2, 4, 8]),
        case((1 << 29), [(1 << 29) - 1]),
    ]
    w.add(multi(edge))
    # small random, tiny bit-widths (lots of overlap)
    for bits in (2, 4, 8):
        hi = (1 << bits) - 1
        cases = [case(rnd.randint(0, hi),
                      [rnd.randint(0, hi) for _ in range(rnd.randint(1, 8))])
                 for _ in range(100)]
        w.add(multi(cases))
    # full-range randoms
    for _ in range(3):
        cases = [case(rnd.randint(0, MAX),
                      [rnd.randint(0, MAX) for _ in range(rnd.randint(1, 100))])
                 for _ in range(50)]
        w.add(multi(cases))
    # max-size: t = 100, sum n = 10^4
    cases = []
    total = 0
    for i in range(100):
        n = 100 if total + 100 <= 10**4 else 10**4 - total
        total += n
        cases.append(case(rnd.randint(0, MAX),
                          [rnd.randint(0, MAX) for _ in range(n)]))
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
