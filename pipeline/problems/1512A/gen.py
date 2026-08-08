import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(rnd, n, pos=None):
    v = rnd.randint(1, 100)
    u = rnd.choice([x for x in range(1, 101) if x != v])
    a = [v] * n
    if pos is None:
        pos = rnd.randrange(n)
    a[pos] = u
    return f"{n}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1512)
    w = Writer(outdir)
    # spy at every position of n=3
    w.add(multi([case(rnd, 3, p) for p in range(3)]))
    # spy at first/last of max n
    w.add(multi([case(rnd, 100, 0), case(rnd, 100, 99), case(rnd, 100, 1), case(rnd, 100, 98)]))
    # random
    for _ in range(4):
        w.add(multi([case(rnd, rnd.randint(3, 100)) for _ in range(100)]))
    # max t, max n
    w.add(multi([case(rnd, 100) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
