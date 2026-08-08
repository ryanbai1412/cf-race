import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXV = 10**9


def case(a, b):
    n = len(a)
    return (f"{n}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)))


def rand_case(rnd, n, max_v=MAXV, p_fire=0.5):
    a = [0 if rnd.random() < p_fire else 1 for _ in range(n)]
    b = [rnd.randint(1, max_v) for _ in range(n)]
    return case(a, b)


def main(outdir):
    rnd = random.Random(1738)
    w = Writer(outdir)
    # edges: n=1 both types, all one type, equal counts, off-by-one counts
    w.add(multi([case([0], [MAXV]), case([1], [1]),
                 case([0] * 5, [MAXV] * 5), case([1] * 5, [MAXV] * 5),
                 case([0, 1], [MAXV, MAXV]),
                 case([0, 1, 0], [5, 5, 5]),
                 case([0] * 3 + [1] * 3, [MAXV] * 6),
                 case([0] * 4 + [1] * 3, [1, 2, 3, 4, 5, 6, 7])]))
    # small random, mixed values (overflow-safe check: values up to 1e9)
    w.add(multi([rand_case(rnd, rnd.randint(1, 6), max_v=10)
                 for _ in range(2000)]))
    w.add(multi([rand_case(rnd, rnd.randint(1, 10)) for _ in range(2000)]))
    # skewed type distributions
    w.add(multi([rand_case(rnd, rnd.randint(1, 50), p_fire=0.9)
                 for _ in range(1000)]))
    w.add(multi([rand_case(rnd, rnd.randint(1, 50), p_fire=0.1)
                 for _ in range(1000)]))
    # max t with tiny cases (values kept small to stay under 1MB)
    w.add(multi([rand_case(rnd, 1, max_v=999) for _ in range(10**5)]))
    # max n single case (small values, keeps file <1MB)
    w.add(multi([rand_case(rnd, 10**5, max_v=999)]))
    # 64-bit overflow tests: max values, large n (answer near 1e14)
    w.add(multi([rand_case(rnd, 4 * 10**4)]))
    w.add(multi([case([0, 1] * (2 * 10**4), [MAXV] * (4 * 10**4))]))


if __name__ == "__main__":
    main(sys.argv[1])
