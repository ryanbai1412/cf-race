import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a):
    return f"{len(a)}\n{' '.join(map(str, a))}"


def main(outdir):
    rnd = random.Random(16911)
    w = Writer(outdir)
    # edge cases: all even, all odd, min n, alternating
    edge = [
        case([2, 4, 6]),
        case([1, 3, 5]),
        case([1, 2, 3]),
        case([2, 1, 2, 1, 2]),
        case([10**9, 10**9 - 1, 10**9]),
        case([1, 1, 2]),
        case([2, 2, 1]),
    ]
    w.add(multi(edge))
    # small random
    for _ in range(5):
        cases = [case([rnd.randint(1, 20) for _ in range(rnd.randint(3, 10))])
                 for _ in range(90)]
        w.add(multi(cases))
    # skewed parity distributions
    for p in (0.05, 0.5, 0.95):
        cases = []
        for _ in range(20):
            n = rnd.randint(3, 500)
            a = [rnd.randint(1, 10**9) // 2 * 2 + (1 if rnd.random() < p else 0)
                 for _ in range(n)]
            a = [max(1, x) for x in a]
            cases.append(case(a))
        w.add(multi(cases))
    # max-size: sum n = 10^5, mixed small/large values, < 1MB
    cases = []
    total = 0
    while total < 10**5 - 2000:
        n = rnd.randint(1000, 4000)
        total += n
        hi = rnd.choice([9, 999, 10**9])
        cases.append(case([rnd.randint(1, hi) for _ in range(n)]))
    w.add(multi(cases))
    # single max case, all huge values (n kept so file < 1MB)
    w.add(multi([case([rnd.randint(10**8, 10**9) for _ in range(80000)])]))


if __name__ == "__main__":
    main(sys.argv[1])
