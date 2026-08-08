import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(n, s):
    return f"{n} {s}"


def make_case(rnd, n, k=None):
    """Build a valid (n, s): k elements equal n^2, rest in [0, n-1]."""
    if k is None:
        k = rnd.randint(0, n + 1)
    rest = n + 1 - k
    s = k * n * n + sum(rnd.randint(0, n - 1) for _ in range(rest))
    return case(n, s)


def main(outdir):
    rnd = random.Random(1646)
    w = Writer(outdir)
    nmax = 10**6 - 1
    # edges: n=1, s=0, all elements n^2, max n
    w.add(multi([case(1, 0), case(1, 2), case(7, 0),
                 case(nmax, (nmax + 1) * nmax * nmax),
                 case(nmax, 0), case(nmax, nmax * nmax)]))
    # boundary: k*n^2 plus max remainder (n-k+1 elements of n-1)
    cases = []
    for n in (2, 3, 10, 1000, nmax):
        for k in (0, 1, n // 2, n, n + 1):
            cases.append(case(n, k * n * n + (n + 1 - k) * (n - 1)))
            cases.append(case(n, k * n * n))
    w.add(multi(cases))
    # random
    for seed in range(6):
        cases = []
        for _ in range(200):
            n = rnd.choice([rnd.randint(1, 10), rnd.randint(1, 1000), rnd.randint(1, nmax)])
            cases.append(make_case(rnd, n))
        w.add(multi(cases))
    # max t small-n stress
    w.add(multi([make_case(rnd, rnd.randint(1, 5)) for _ in range(20000)]))


if __name__ == "__main__":
    main(sys.argv[1])
