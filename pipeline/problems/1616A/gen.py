import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer, multi  # noqa: E402


def case(rnd, n, lo, hi):
    a = [rnd.randint(lo, hi) for _ in range(n)]
    return f"{n}\n" + " ".join(map(str, a))


def main(outdir):
    rnd = random.Random(1616)
    w = Writer(outdir)
    # edges: zeros, all same, single element
    w.add(multi([
        "1\n0",
        "1\n100",
        "1\n-100",
        "5\n0 0 0 0 0",
        "4\n7 7 7 7",
        "6\n-3 -3 3 3 -3 3",
        "3\n0 0 100",
        "100\n" + " ".join(["1"] * 100),
    ]))
    # random tiny value ranges (many collisions)
    for _ in range(4):
        w.add(multi([case(rnd, rnd.randint(1, 20), -3, 3)
                     for _ in range(100)]))
    # random full ranges
    for _ in range(4):
        w.add(multi([case(rnd, rnd.randint(1, 100), -100, 100)
                     for _ in range(100)]))
    # max size
    w.add(multi([case(rnd, 100, -100, 100) for _ in range(100)]))


if __name__ == "__main__":
    main(sys.argv[1])
