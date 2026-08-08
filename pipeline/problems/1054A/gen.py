import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(v):
    return " ".join(map(str, v))


def main(outdir):
    rnd = random.Random(1054)
    w = Writer(outdir)
    # boundary / extreme configurations
    w.add(case([1, 2, 1, 1, 1, 1]))
    w.add(case([1, 1000, 1000, 1000, 1000, 1000]))
    w.add(case([1000, 1, 1, 1000, 1, 1]))
    w.add(case([1, 2, 1000, 1, 1000, 1000]))
    w.add(case([500, 501, 500, 1000, 1, 1]))
    w.add(case([1, 1000, 1, 1, 1, 1]))
    # exact-tie cases (elevator time == stairs time -> YES)
    for x, y, z, t2, t3 in [(1, 5, 1, 1, 1), (3, 9, 3, 2, 4), (10, 4, 10, 3, 5)]:
        ele = (abs(z - x) + abs(x - y)) * t2 + 3 * t3
        d = abs(x - y)
        if ele % d == 0 and 1 <= ele // d <= 1000:
            w.add(case([x, y, z, ele // d, t2, t3]))
    # random small and random full-range
    for _ in range(6):
        x = rnd.randint(1, 10)
        y = rnd.randint(1, 10)
        while y == x:
            y = rnd.randint(1, 10)
        w.add(case([x, y, rnd.randint(1, 10)] + [rnd.randint(1, 10) for _ in range(3)]))
    for _ in range(5):
        x = rnd.randint(1, 1000)
        y = rnd.randint(1, 1000)
        while y == x:
            y = rnd.randint(1, 1000)
        w.add(case([x, y, rnd.randint(1, 1000)] + [rnd.randint(1, 1000) for _ in range(3)]))


if __name__ == "__main__":
    main(sys.argv[1])
