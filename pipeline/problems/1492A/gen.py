import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

BIG = 10 ** 18


def case(p, a, b, c):
    return f"{p} {a} {b} {c}"


def main(outdir):
    rnd = random.Random(1492)
    w = Writer(outdir)

    # edge cases: minimum/maximum values, exact arrivals, 64-bit overflow traps
    w.add(multi([
        case(1, 1, 1, 1),
        case(BIG, BIG, BIG, BIG),
        case(BIG, 1, 1, 1),
        case(1, BIG, BIG, BIG),
        case(BIG - 1, BIG, BIG, BIG),
        case(BIG, BIG - 1, BIG, BIG),
        case(BIG, 999999999999999999, 1000000000000000000, 999999999999999998),
        case(10, 2, 5, 10),                       # exact arrival -> 0
        case(10, 9, 9, 9),
        case(2, 6, 10, 9),
    ]))

    # small random tests
    for _ in range(4):
        cases = [case(rnd.randint(1, 30), rnd.randint(1, 12), rnd.randint(1, 12),
                      rnd.randint(1, 12)) for _ in range(rnd.randint(1, 100))]
        w.add(multi(cases))

    # random tests with mixed magnitudes
    for _ in range(3):
        cases = []
        for _ in range(rnd.randint(100, 1000)):
            def r():
                return rnd.randint(1, 10 ** rnd.randint(0, 18))
            cases.append(case(r(), r(), r(), r()))
        w.add(multi(cases))

    # exact multiples (answer 0) and one-short cases mixed
    cases = []
    for _ in range(500):
        a = rnd.randint(1, 10 ** 9)
        k = rnd.randint(1, 10 ** 9)
        p = a * k
        cases.append(case(p, a, rnd.randint(1, 10 ** 18), rnd.randint(1, 10 ** 18)))
        cases.append(case(p - 1 if p > 1 else 1, a, rnd.randint(1, 10 ** 18),
                          rnd.randint(1, 10 ** 18)))
    w.add(multi(cases))

    # max t with max magnitudes
    cases = [case(rnd.randint(10 ** 17, BIG), rnd.randint(10 ** 17, BIG),
                  rnd.randint(10 ** 17, BIG), rnd.randint(10 ** 17, BIG))
             for _ in range(1000)]
    w.add(multi(cases))


if __name__ == "__main__":
    main(sys.argv[1])
