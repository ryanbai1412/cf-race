import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

MAXV = 10**9


def case(rects):
    return f"{len(rects)}\n" + "\n".join(f"{a} {b}" for a, b in rects)


def rand_case(rnd, n, max_v=MAXV):
    return case([(rnd.randint(1, max_v), rnd.randint(1, max_v))
                 for _ in range(n)])


def main(outdir):
    rnd = random.Random(1740)
    w = Writer(outdir)
    # edges: n=1, squares, extreme values (answer up to ~4e14: needs 64-bit)
    w.add(multi([case([(1, 1)]), case([(MAXV, MAXV)]), case([(1, MAXV)]),
                 case([(MAXV, 1)] * 5), case([(1, 1)] * 5),
                 case([(MAXV, MAXV)] * 5),
                 case([(3, 5), (5, 3)])]))
    # small random
    w.add(multi([rand_case(rnd, rnd.randint(1, 5), max_v=10)
                 for _ in range(2000)]))
    w.add(multi([rand_case(rnd, rnd.randint(1, 8)) for _ in range(2000)]))
    # max t with n=1 (small values, keeps file <1MB)
    w.add(multi([rand_case(rnd, 1, max_v=999) for _ in range(2 * 10**4)]))
    # max total n (small values, keeps file <1MB)
    w.add(multi([rand_case(rnd, 2 * 10**5, max_v=9)]))
    # 64-bit overflow test: max values, large n (answer near 1e14)
    w.add(multi([case([(MAXV, MAXV)] * (4 * 10**4))]))


if __name__ == "__main__":
    main(sys.argv[1])
