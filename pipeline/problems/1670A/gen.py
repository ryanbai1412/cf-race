import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXV = 10**9


def fmt(a):
    return f"{len(a)}\n{' '.join(map(str, a))}"


def rand_case(rnd, n, lo=1, hi=MAXV):
    a = []
    for _ in range(n):
        v = rnd.randint(lo, hi)
        a.append(v if rnd.random() < 0.5 else -v)
    return fmt(a)


def yes_case(rnd, n):
    # sorted abs values with negatives packed in front
    vals = sorted(rnd.randint(1, MAXV) for _ in range(n))
    k = rnd.randint(0, n)
    a = [-vals[i] if i < k else vals[i] for i in range(n)]
    # negatives must be in decreasing abs order to be non-decreasing
    neg = sorted((abs(x) for x in a[:k]), reverse=True)
    a = [-x for x in neg] + a[k:]
    a = sorted(a)
    # shuffle signs across positions with same neg count keeps reachability
    rnd.shuffle(a)
    k2 = sum(1 for x in a if x < 0)
    b = sorted(abs(x) for x in a)
    return fmt([-b[i] if i < k2 else b[i] for i in range(n)])


def main(outdir):
    rnd = random.Random(1670)
    w = Writer(outdir)
    # n=1 and tiny edges
    w.add(multi(["1\n5", "1\n-5", "2\n-1 1", "2\n1 -1", "2\n-1000000000 1000000000"]))
    # small random with tiny values (many duplicates/ties)
    w.add(multi([rand_case(rnd, rnd.randint(1, 6), 1, 3) for _ in range(300)]))
    # constructed YES cases (result of the greedy assignment)
    w.add(multi([yes_case(rnd, rnd.randint(1, 20)) for _ in range(100)]))
    # random medium
    for _ in range(3):
        w.add(multi([rand_case(rnd, rnd.randint(1, 100)) for _ in range(100)]))
    # max size: sum n = 1e5 in one case + spread cases
    w.add(multi([rand_case(rnd, 100000, 1, 10)]))
    w.add(multi([rand_case(rnd, 100) for _ in range(1000)]))


if __name__ == "__main__":
    main(sys.argv[1])
