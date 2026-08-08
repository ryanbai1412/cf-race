import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(a, queries):
    lines = [f"{len(a)} {len(queries)}", " ".join(map(str, a))]
    lines += [f"{t} {x}" for t, x in queries]
    return "\n".join(lines)


def rand_case(rnd, n, q, amax=10**9, xmax=10**4):
    a = [rnd.randint(1, amax) for _ in range(n)]
    qs = [(rnd.randint(0, 1), rnd.randint(1, xmax)) for _ in range(q)]
    return case(a, qs)


def main(outdir):
    rnd = random.Random(1744)
    w = Writer(outdir)
    # edges: n=q=1, all max values, all-even array, all-odd array
    w.add(multi([case([1], [(0, 1)]), case([10**9] * 5, [(0, 10**4)] * 5),
                 case([2] * 10, [(1, 3), (0, 3), (1, 2), (0, 2)]),
                 case([1] * 10, [(0, 1), (1, 1), (0, 1), (1, 1)])]))
    # max size: n=q=1e5 single case, max values (overflow trap)
    w.add(multi([rand_case(rnd, 10**5, 10**5)]))
    # many small cases summing near limits
    w.add(multi([rand_case(rnd, rnd.randint(1, 200), rnd.randint(1, 200)) for _ in range(500)]))
    # small-value randoms
    for _ in range(7):
        w.add(multi([rand_case(rnd, rnd.randint(1, 8), rnd.randint(1, 8), amax=10, xmax=3)
                     for _ in range(rnd.randint(1, 20))]))


if __name__ == "__main__":
    main(sys.argv[1])
