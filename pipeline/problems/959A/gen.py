import random
import sys

sys.path.insert(0, "/home/ubuntu/repos/cf-race/pipeline")
from genlib import Writer  # noqa: E402


def main(outdir):
    rnd = random.Random(959)
    w = Writer(outdir)
    # edges
    for v in (1, 2, 3, 4, 999999999, 1000000000):
        w.add(str(v))
    # random small and large
    for _ in range(6):
        w.add(str(rnd.randint(1, 100)))
    for _ in range(6):
        w.add(str(rnd.randint(1, 10**9)))


if __name__ == "__main__":
    main(sys.argv[1])
