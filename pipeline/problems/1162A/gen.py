import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402

MAX = 50


def case(n, h, restr):
    lines = [f"{n} {h} {len(restr)}"]
    lines += [f"{l} {r} {x}" for l, r, x in restr]
    return "\n".join(lines) + "\n"


def main(outdir):
    rnd = random.Random(1162)
    w = Writer(outdir)
    # smallest
    w.add(case(1, 1, [(1, 1, 0)]))
    w.add(case(1, 1, [(1, 1, 1)]))
    # all restrictions are x=0 (profit 0)
    w.add(case(MAX, MAX, [(1, MAX, 0)] * MAX))
    # single wide non-binding restriction
    w.add(case(MAX, MAX, [(1, MAX, MAX)] * MAX))
    # nested restrictions tightening the middle
    w.add(case(MAX, MAX, [(i + 1, MAX - i, MAX - i) for i in range(MAX // 2)]))
    # per-spot restrictions with increasing caps
    w.add(case(MAX, MAX, [(i + 1, i + 1, i % (MAX + 1)) for i in range(MAX)]))
    # overlapping duplicates on one spot
    w.add(case(MAX, MAX, [(1, 1, x) for x in range(MAX)]))
    # random small (brute-force checkable)
    for _ in range(6):
        n = rnd.randint(1, 4)
        h = rnd.randint(0, 3) or 1
        m = rnd.randint(1, 4)
        restr = []
        for _ in range(m):
            lo = rnd.randint(1, n)
            hi = rnd.randint(lo, n)
            restr.append((lo, hi, rnd.randint(0, h)))
        w.add(case(n, h, restr))
    # random max size
    for _ in range(4):
        n, h, m = MAX, MAX, MAX
        restr = []
        for _ in range(m):
            lo = rnd.randint(1, n)
            hi = rnd.randint(lo, n)
            restr.append((lo, hi, rnd.randint(0, h)))
        w.add(case(n, h, restr))


if __name__ == "__main__":
    main(sys.argv[1])
