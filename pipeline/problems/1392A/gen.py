import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXV = 10**9


def case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1392)
    w = Writer(outdir)

    # minimal input
    w.add(multi([case([1])]))
    # large all-equal array (answer n) and one large random array
    # N is capped so each input file stays under 1 MB
    N = 80000
    w.add(multi([case([MAXV] * N)]))
    w.add(multi([case([rnd.randint(1, MAXV) for _ in range(N)])]))
    # max-size array that is equal except the last element
    a = [7] * N
    a[-1] = 8
    w.add(multi([case(a)]))
    # 100 test cases, each all-equal, sizes summing to N
    cases = []
    rem = N
    for i in range(100):
        n = rem // (100 - i)
        cases.append(case([rnd.randint(1, MAXV)] * n))
        rem -= n
    w.add(multi(cases))
    # small arrays: all n=1..2 and mixes of equal/unequal
    w.add(multi([case([1]), case([1, 1]), case([1, 2]), case([2, 2, 2]),
                 case([2, 2, 3]), case([5, 5, 5, 5, 5])]))
    # random small tests
    for _ in range(10):
        t = rnd.randint(1, 100)
        cs = []
        for _ in range(t):
            n = rnd.randint(1, 8)
            hi = rnd.choice([1, 2, 3, MAXV])
            cs.append(case([rnd.randint(1, hi) for _ in range(n)]))
        w.add(multi(cs))


if __name__ == "__main__":
    main(sys.argv[1])
