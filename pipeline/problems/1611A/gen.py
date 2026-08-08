import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402

ODD = "13579"
EVEN = "2468"
NONZERO = "123456789"


def rand_num(rnd, max_len=9):
    return "".join(rnd.choice(NONZERO) for _ in range(rnd.randint(1, max_len)))


def main(outdir):
    rnd = random.Random(1611)
    w = Writer(outdir)
    # edge: each answer class, single digits, max length
    w.add(multi([
        "2",            # 0 ops
        "3",            # -1
        "12",           # 0 ops
        "21",           # 1 op (first digit even)
        "13",           # -1 (no even digit)
        "121",          # 2 ops (even digit in middle)
        "999999998",    # 1 op? last is 8 -> 0 ops
        "899999999",    # first even -> 1 op
        "998999999",    # even inside -> 2 ops
        "111111111",    # -1
        "222222222",    # 0
    ]))
    # exhaustive 1-2 digit numbers
    one_two = [str(x) for x in range(1, 100) if "0" not in str(x)]
    w.add(multi(one_two))
    # random by class: all-odd, ends even, starts even, even inside only
    def all_odd(rnd):
        return "".join(rnd.choice(ODD) for _ in range(rnd.randint(1, 9)))

    def ends_even(rnd):
        return rand_num(rnd, 8) + rnd.choice(EVEN)

    def starts_even(rnd):
        return rnd.choice(EVEN) + "".join(rnd.choice(ODD) for _ in range(rnd.randint(1, 8)))

    def even_inside(rnd):
        n = rnd.randint(3, 9)
        mid = rnd.randint(1, n - 2)
        digs = [rnd.choice(ODD) for _ in range(n)]
        digs[mid] = rnd.choice(EVEN)
        return "".join(digs)

    for f in (all_odd, ends_even, starts_even, even_inside):
        w.add(multi([f(rnd) for f2 in range(2000)]))
    # random mixed
    for _ in range(3):
        w.add(multi([rand_num(rnd) for _ in range(5000)]))
    # max-size: t = 10^4
    w.add(multi([rand_num(rnd) for _ in range(10**4)]))


if __name__ == "__main__":
    main(sys.argv[1])
